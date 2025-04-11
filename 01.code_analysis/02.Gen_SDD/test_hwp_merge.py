from pyhwpx import Hwp

def insert_template_file(path):
    hwpx.insert_file(path)

hwpx = Hwp(new=True, visible=False)

insert_template_file(f"C:/Users/ypelec/Desktop/SDD_manual_control/ManualControl.cpp.hwp")
insert_template_file(f"C:/Users/ypelec/Desktop/SDD_manual_control/ManualControlSelector.cpp.hwp")
insert_template_file(f"C:/Users/ypelec/Desktop/SDD_manual_control/ManualControlSelector.hpp.hwp")
insert_template_file(f"C:/Users/ypelec/Desktop/SDD_manual_control/MovingDiff.hpp.hwp")

save_file_name = "CSU_수동조종입력"
save_file_path = f"C:/Users/ypelec/Desktop/{save_file_name}.hwp"
hwpx.SaveAs(save_file_path)
hwpx.clear()
