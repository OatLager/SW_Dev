import os
from . import mav_parse


def mavgen(opts, args):

    xml = []
    all_files = set()

    # xml 파일 내부에 다른 xml 파일을 참조하는 경우 확장하여 포함시킴
    def expand_includes():

        def expand_oneiteration():

            includeadded = False
            for x in xml[:]:
                for i in x.include:
                    fname = os.path.abspath(os.path.join(os.path.dirname(x.filename), i))
                    # Only parse new include files
                    if fname in all_files:
                        continue
                    print("Parsing %s" % fname)
                    xml.append(mav_parse.MAVXML(fname, opts.wire_protocol))
                    all_files.add(fname)
                    includeadded = True
            return includeadded

        for i in range(opts.max_include_file):
            if not expand_oneiteration():
                break

        if mav_parse.check_duplicates(xml):
            return False
        return True

    def update_includes():

        # 1: Mark files that don't have includes as "done"
        done = []
        for x in xml:
            #print("\n",x)
            if len(x.include) == 0:
                done.append(x)
                print("\nFile with no includes found (ENDPOINT): %s" % x.filename )
        if len(done) == 0:
            print("\nERROR in includes tree, no base found!")
            exit(1)

        #print("\n",done)

        # 2: Update all 'not done' files for which all includes have
        # been done.  Returns True if any updates were made
        def update_oneiteration():
            initial_done_length = len(done)
            for x in xml:
                #print("\nCHECK %s" % x.filename)
                if x in done:
                    #print("  already done, skip")
                    continue
                #check if all its includes were already done
                all_includes_done = True
                for i in x.include:
                    fname = os.path.abspath(os.path.join(os.path.dirname(x.filename), i))
                    if fname not in [d.filename for d in done]:
                        all_includes_done = False
                        break
                if not all_includes_done:
                    #print("  not all includes ready, skip")
                    continue
                #Found file where all includes are done
                done.append(x)
                #print("  all includes ready, add" )
                #now update it with the facts from all it's includes
                for i in x.include:
                    fname = os.path.abspath(os.path.join(os.path.dirname(x.filename), i))
                    #print("  include file %s" % i )
                    #Find the corresponding x
                    for ix in xml:
                        if ix.filename != fname:
                            continue
                        #print("    add %s" % ix.filename )
                        x.message_crcs.update(ix.message_crcs)
                        x.message_lengths.update(ix.message_lengths)
                        x.message_min_lengths.update(ix.message_min_lengths)
                        x.message_flags.update(ix.message_flags)
                        x.message_target_system_ofs.update(ix.message_target_system_ofs)
                        x.message_target_component_ofs.update(ix.message_target_component_ofs)
                        x.message_names.update(ix.message_names)
                        x.largest_payload = max(x.largest_payload, ix.largest_payload)
                        break

            if len(done) == len(xml):
                return False  # finished
            if len(done) == initial_done_length:
                # we've made no progress
                print("ERROR include tree can't be resolved, no base found!")
                exit(1)
            return True

        for i in range(opts.max_include_file):
            #print("\nITERATION "+str(i))
            if not update_oneiteration():
                break

    # Process all XML files, validating them as necessary.
    for fname in args:
        # only add each dialect file argument once.
        if fname in all_files:
            continue
        all_files.add(fname)
        print("Parsing %s" % fname)
        xml.append(mav_parse.MAVXML(fname, opts.wire_protocol))

    # expand includes
    if not expand_includes():
        return False
    update_includes()

    print("Found %u MAVLink message types in %u XML files" % (
        mav_parse.total_msgs(xml), len(xml)))

    #convert language option to lowercase and validate
    opts.language = opts.language.lower()
    # C language Code Generation - [mavgen_c.py]  
    if  opts.language == 'c':
        from .Language.C import mav_gen_c
        mav_gen_c.generate(opts.output, xml)
    else:
        print("Unsupported language %s" % opts.language)

    return True

