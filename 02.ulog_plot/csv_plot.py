import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.dates as mdates
import numpy as np
# import subprocess
import threading
from pyulog import ULog
from pyulog.ulog2csv import convert_ulog2csv
import csv
# from datetime import datetime, timedelta

class CSVViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Viewer")
        self.root.geometry("1200x800")

        # Initialize variables
        self.folder_path = ""
        self.df = None
        self.all_csv_files = []
        self.current_file = None
        self.selected_columns = []
        self.cursor_enabled = False
        self.cursor_locked = False
        self._cid_motion = None
        self._cid_click = None
        self.markers = []
        self.lines = []
        self.vline = None
        self.text = None
        self.last_cursor_x = None
        self.last_mouse_x = None
        self.x_column = None
        self.fig = None
        self.ax = None
        self.canvas = None
        
        # Create main frames
        self.left_frame = tk.Frame(root, width=400)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.right_frame = tk.Frame(root)
        self.right_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Create and pack widgets for the left frame
        self.create_left_frame_widgets()

        # Create notebook (tabbed interface) for the right frame
        self.create_notebook()
        self.create_graph()

        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Bind space key for cursor lock toggle
        self.root.bind('<space>', self.toggle_cursor_lock)
        
    def create_left_frame_widgets(self):
        # File operations
        file_frame = tk.LabelFrame(self.left_frame, text="File")
        file_frame.pack(fill=tk.X, padx=5, pady=5)

        self.convert_button = tk.Button(file_frame, text="Convert", command=self.convert_ulog)
        self.convert_button.pack(fill=tk.X, padx=5, pady=2)

        self.load_button = tk.Button(file_frame, text="Load", command=self.select_folder)
        self.load_button.pack(fill=tk.X, padx=5, pady=2)

        # CSV file selection
        csv_frame = tk.LabelFrame(self.left_frame, text="CSV Files")
        csv_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.search_entry = tk.Entry(csv_frame)
        self.search_entry.pack(fill=tk.X, padx=5, pady=2)
        self.search_entry.bind("<KeyRelease>", self.search_and_update_tree)

        # Create a frame to hold the tree and scrollbars
        tree_frame = ttk.Frame(csv_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)

        # Create the treeview
        self.csv_tree = ttk.Treeview(tree_frame, show="tree", selectmode="extended")
        
        # Create vertical scrollbar
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.csv_tree.yview)
        vsb.pack(side='right', fill='y')

        # Create horizontal scrollbar
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.csv_tree.xview)
        hsb.pack(side='bottom', fill='x')

        # Configure the treeview
        self.csv_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.csv_tree.pack(side='left', fill=tk.BOTH, expand=True)

        # Configure the treeview column
        self.csv_tree.column("#0", width=200, stretch=tk.NO)

        self.csv_tree.bind('<Double-1>', self.on_item_double_click)
        self.csv_tree.bind('<<TreeviewSelect>>', self.on_select_csv)

        # Use Timestamp 버튼 추가
        self.use_timestamp = tk.BooleanVar(value=False)
        self.use_timestamp_button = ttk.Checkbutton(
            self.left_frame,
            text="Use Timestamp as X-axis",
            variable=self.use_timestamp,
            command=self.toggle_x_axis
        )
        self.use_timestamp_button.pack(pady=5)

        # Cursor toggle button
        self.cursor_button = tk.Button(self.left_frame, text="Enable Cursor", command=self.toggle_cursor, state=tk.DISABLED)
        self.cursor_button.pack(fill=tk.X, padx=5, pady=2)

        # Background Color 섹션 추가
        bg_frame = tk.LabelFrame(self.left_frame, text="Background Color")
        bg_frame.pack(fill=tk.X, padx=5, pady=5)

        # CSV 파일 선택 드롭다운
        tk.Label(bg_frame, text="CSV File:").pack(anchor='w')
        self.bg_csv_combobox = ttk.Combobox(bg_frame, state="readonly")
        self.bg_csv_combobox.pack(fill=tk.X, padx=5, pady=2)
        self.bg_csv_combobox.bind("<<ComboboxSelected>>", self.update_bg_data_combobox)

        # CSV 데이터 선택 드롭다운
        tk.Label(bg_frame, text="Data Column:").pack(anchor='w')
        self.bg_data_combobox = ttk.Combobox(bg_frame, state="readonly")
        self.bg_data_combobox.pack(fill=tk.X, padx=5, pady=2)

        # 배경색 적용/해제 버튼
        self.bg_apply_button = tk.Button(bg_frame, text="Apply Background", command=self.toggle_background, state=tk.DISABLED)
        self.bg_apply_button.pack(fill=tk.X, padx=5, pady=2)

        self.background_applied = False

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Tab 1")

    def create_graph(self):
        # 그래프 프레임 생성
        self.graph_frame = ttk.Frame(self.tab1)
        self.graph_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # 데이터 테이블 프레임 생성
        self.table_frame = ttk.Frame(self.tab1)
        self.table_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # 그래프 생성
        self.fig = Figure(figsize=(8, 4))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # 이벤트 바인딩 추가
        self.canvas.mpl_connect('button_press_event', self.on_graph_click)
        self.root.bind('<space>', self.toggle_cursor_lock)
        
        toolbar = NavigationToolbar2Tk(self.canvas, self.graph_frame)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        print("Graph created")  # 디버깅을 위한 출력

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.all_csv_files = [f for f in os.listdir(self.folder_path) if f.endswith('.csv')]
            self.update_csv_tree()
            self.update_bg_csv_combobox()

    def update_csv_tree(self):
        self.csv_tree.delete(*self.csv_tree.get_children())
        max_width = 200  # 초기 최대 너비

        for file in self.all_csv_files:
            file_item = self.csv_tree.insert('', 'end', text=file)
            max_width = max(max_width, len(file) * 7)  # 대략적인 픽셀 너비 계산
            df = pd.read_csv(os.path.join(self.folder_path, file))
            for column in df.columns:
                self.csv_tree.insert(file_item, 'end', text=column)
                max_width = max(max_width, len(column) * 7)

        # 열 너비 조정
        self.csv_tree.column("#0", width=max_width, stretch=tk.NO)

    def search_and_update_tree(self, event):
        search_term = self.search_entry.get().lower()
        self.csv_tree.delete(*self.csv_tree.get_children())
        for file in self.all_csv_files:
            if search_term in file.lower():
                file_item = self.csv_tree.insert('', 'end', text=file)
                df = pd.read_csv(os.path.join(self.folder_path, file))
                for column in df.columns:
                    if search_term in column.lower():
                        self.csv_tree.insert(file_item, 'end', text=column)

    def on_item_double_click(self, event):
        item = self.csv_tree.selection()[0]
        parent = self.csv_tree.parent(item)
        if parent:  # This is a column
            file_name = self.csv_tree.item(parent)['text']
            column_name = self.csv_tree.item(item)['text']
            self.plot_column(file_name, column_name)

    def plot_column(self, file_name, column_name):
        file_path = os.path.join(self.folder_path, file_name)
        df = pd.read_csv(file_path)
        
        if 'timestamp' in df.columns:
            x = df['timestamp']
            y = df[column_name]
            
            self.ax.clear()
            self.ax.plot(x, y)
            self.ax.set_xlabel('Timestamp')
            self.ax.set_ylabel(column_name)
            self.ax.set_title(f'{self.current_file}')
            self.canvas.draw()

    def toggle_x_axis(self):
        print(f"Toggle X-axis called. Use timestamp: {self.use_timestamp.get()}")  # 디버그 출력
        
        all_columns = [self.x_column] + self.selected_columns if self.x_column else self.selected_columns
        all_columns = [col for col in all_columns if col is not None]

        if not all_columns:
            return  # 선택된 열이 없으면 아무 것도 하지 않음

        if self.use_timestamp.get():
            # timestamp를 x축으로 사용
            if 'timestamp' in self.df.columns:
                self.x_column = 'timestamp'
                self.selected_columns = [col for col in all_columns if col != 'timestamp']
                self.cursor_button.config(state=tk.NORMAL)  # 커서 버튼 활성화
                self.bg_apply_button.config(state=tk.NORMAL)  # 배경색 버튼 활성화
            else:
                messagebox.showwarning("Warning", "No timestamp column found in the data.")
                self.use_timestamp.set(False)
                self.cursor_button.config(state=tk.DISABLED)  # 커서 버튼 비활성화
                self.bg_apply_button.config(state=tk.DISABLED)  # 배경색 버튼 비활성화
                return
        else:
            # timestamp를 x축에서 제거하고 첫 번째 선택된 열을 x축으로 사용
            if 'timestamp' in all_columns:
                all_columns.remove('timestamp')
            if all_columns:
                self.x_column = all_columns[0]
                self.selected_columns = all_columns[1:]
            else:
                self.x_column = None
                self.selected_columns = []
            self.cursor_button.config(state=tk.DISABLED)  # 커서 버튼 비활성화
            self.bg_apply_button.config(state=tk.DISABLED)  # 배경색 버튼 비활성화
            self.cursor_enabled = False
            self.cursor_locked = False
            self.background_applied = False
            self.reset_background()  # 배경색 설정 리셋

        print(f"After toggle - X-axis: {self.x_column}, Selected columns: {self.selected_columns}")  # 디버그 출력
        
        self.plot_selected_columns()
        self.display_selected_columns()

        # 커서 버튼과 배경색 버튼의 텍스트를 초기 상태로 변경
        self.cursor_button.config(text="Enable Cursor")
        self.bg_apply_button.config(text="Apply Background")

    def on_select_csv(self, event):
        selected_items = self.csv_tree.selection()
        if not selected_items:
            return

        item = selected_items[0]
        parent = self.csv_tree.parent(item)
        
        if parent == '':  # It's a root item (CSV file)
            file_name = self.csv_tree.item(item)['text']
            if self.current_file is None or file_name != self.current_file:
                self.load_csv_data(file_name)
            self.x_column = None
            self.selected_columns = []
            self.reset_background()  # 배경색 설정 리셋
            return

        # 파일 내부의 데이터(열) 선택 시
        file_name = self.csv_tree.item(parent)['text']
        
        if self.current_file is None or file_name != self.current_file:
            self.load_csv_data(file_name)

        newly_selected_columns = [self.csv_tree.item(item)['text'] for item in selected_items]
        
        if self.use_timestamp.get() and 'timestamp' in self.df.columns:
            self.x_column = 'timestamp'
            self.selected_columns = [col for col in newly_selected_columns if col != 'timestamp']
        else:
            if 'timestamp' in newly_selected_columns:
                newly_selected_columns.remove('timestamp')
            if newly_selected_columns:
                self.x_column = newly_selected_columns[0]
                self.selected_columns = newly_selected_columns[1:]
            else:
                self.x_column = None
                self.selected_columns = []

        print(f"On select - X-axis: {self.x_column}, Selected columns: {self.selected_columns}")

        self.plot_selected_columns()
        self.display_selected_columns()

    def load_csv_data(self, file_name):
        file_path = os.path.join(self.folder_path, file_name)
        try:
            self.df = pd.read_csv(file_path)
            self.current_file = file_name
            
            if 'timestamp' in self.df.columns:
                self.df['timestamp'] = (self.df['timestamp'] * 1e-6).round(3)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV data: {str(e)}")

    def toggle_cursor(self):
        self.cursor_enabled = not self.cursor_enabled
        self.cursor_locked = False
        
        print(f"Cursor {'enabled' if self.cursor_enabled else 'disabled'}")
        # # 배경 상태를 저장
        # background_state = self.background_applied
        # bg_data = self.bg_data
        
        # self.plot_selected_columns()
        
        # # 배경 상태를 복원
        # self.background_applied = background_state
        # self.bg_data = bg_data
        if self.cursor_enabled:
            self.cursor_button.config(text="Disable Cursor")
            self.plot_selected_columns()
            if self.df is not None and self.x_column is not None:
                initial_x = self.df[self.x_column].iloc[0]
                self.last_cursor_x = initial_x  # 초기 위치 설정
                self.update_cursor(initial_x)
        else:
            self.cursor_button.config(text="Enable Cursor")
            if self.vline:
                self.vline.remove()
                self.vline = None
            for marker in self.markers:
                marker.remove()
                if hasattr(marker, 'vline'):
                    marker.vline.remove()
            self.markers = []
            if self.text:
                self.text.remove()
                self.text = None
            self.canvas.draw()
        
        print(f"Cursor toggle complete. Enabled: {self.cursor_enabled}")

    def plot_selected_columns(self):
        print(f"Plotting - X-axis: {self.x_column}, Selected columns: {self.selected_columns}")
        
        if self.df is None or self.x_column is None or not self.selected_columns:
            return

        self.ax.clear()

        # Draw background
        if self.background_applied and self.bg_data is not None and self.df is not None:
            try:
                current_timestamps = self.df[self.x_column].values
                bg_timestamps = self.bg_data['timestamp'].values
                
                current_min, current_max = current_timestamps.min(), current_timestamps.max()
                bg_min, bg_max = bg_timestamps.min(), bg_timestamps.max()
                
                common_min = max(current_min, bg_min)
                common_max = min(current_max, bg_max)
                
                y_max = self.ax.get_ylim()[1]  # 그래프의 y축 최대값
                
                for i in range(len(self.bg_data) - 1):
                    start = self.bg_data['timestamp'].iloc[i]
                    end = self.bg_data['timestamp'].iloc[i+1]
                    color = self.bg_data['color'].iloc[i]
                    value = self.bg_data[self.bg_column].iloc[i]
                    
                    if start <= common_max and end >= common_min:
                        start_idx = np.searchsorted(current_timestamps, max(start, common_min))
                        end_idx = np.searchsorted(current_timestamps, min(end, common_max))
                        
                        if start_idx < len(current_timestamps) and start_idx < end_idx:
                            actual_start = current_timestamps[start_idx]
                            actual_end = current_timestamps[min(end_idx, len(current_timestamps) - 1)]
                            
                            self.ax.axvspan(actual_start, actual_end, facecolor=color, alpha=0.3, zorder=0)
                            
                            # 데이터 값 표시
                            label_x = actual_start
                            label_y = y_max
                            label_text = f'{self.bg_column} = {value}'
                            self.ax.text(label_x, label_y, label_text, 
                                        verticalalignment='top', horizontalalignment='left',
                                        fontsize=8, alpha=0.6)
                
                print(f"\nCurrent data range: {current_min:.6f} to {current_max:.6f}")
                print(f"Background data range: {bg_min:.6f} to {bg_max:.6f}")
                print(f"Common range: {common_min:.6f} to {common_max:.6f}")
            except Exception as e:
                print(f"Error drawing background: {str(e)}")

        # Plot lines
        self.lines = []
        for column in self.selected_columns:
            if column in self.df.columns and column != self.x_column:
                line, = self.ax.plot(self.df[self.x_column], self.df[column], label=column)
                self.lines.append(line)

        self.ax.set_xlabel(self.x_column)
        self.ax.set_ylabel('Values')
        self.ax.set_title(f'{self.current_file}')
        self.ax.legend()
        self.ax.grid(True)

        # Set x-axis range
        self.ax.set_xlim(self.df[self.x_column].min(), self.df[self.x_column].max())

        # Auto-adjust y-axis range
        self.ax.autoscale(axis='y')

        # Set datetime format for x-axis if it's datetime
        if pd.api.types.is_datetime64_any_dtype(self.df[self.x_column]):
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
            self.fig.autofmt_xdate()

        if self.cursor_enabled and self.use_timestamp.get():
            print("Cursor is enabled and timestamp is used")
            
            # Get the first timestamp of the selected data
            initial_x = self.df[self.x_column].iloc[0]
            
            # Create main vline
            if not hasattr(self, 'vline') or self.vline not in self.ax.lines:
                self.vline = self.ax.axvline(x=initial_x, color='r', linestyle='--', linewidth=1, zorder=10)
                print("Created main vline")
            
            # Create or update markers and individual vlines
            self.markers = []
            for line in self.lines:
                y_initial = line.get_ydata()[0]  # Get the first y value for this line
                marker, = self.ax.plot([initial_x], [y_initial], 'o', color=line.get_color(), markersize=6, zorder=11)
                marker.vline = self.ax.axvline(x=initial_x, color=line.get_color(), alpha=0.5, linewidth=0.5, zorder=9)
                self.markers.append(marker)
            print(f"Created {len(self.markers)} new markers with individual vlines")
            
            # Create or update text annotation
            if not hasattr(self, 'text') or self.text not in self.ax.texts:
                self.text = self.ax.text(0.02, 0.98, '', transform=self.ax.transAxes,
                                        verticalalignment='top', horizontalalignment='left',
                                        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
                                        fontsize=9, multialignment='left')
                print("Created new text annotation")
            
            # Initialize cursor position
            self.update_cursor(initial_x)

            def on_mouse_move(event):
                if event.inaxes and not self.cursor_locked:
                    self.update_cursor(event.xdata)

            def on_mouse_click(event):
                if event.inaxes:
                    if event.button == 1:  # 왼쪽 클릭
                        self.lock_cursor(event.xdata)
                    elif event.button == 3:  # 오른쪽 클릭
                        self.unlock_cursor()

            # Remove existing event connections
            if hasattr(self, '_cid_motion'):
                self.fig.canvas.mpl_disconnect(self._cid_motion)
            if hasattr(self, '_cid_click'):
                self.fig.canvas.mpl_disconnect(self._cid_click)

            # Add new event connections
            self._cid_motion = self.fig.canvas.mpl_connect('motion_notify_event', on_mouse_move)
            self._cid_click = self.fig.canvas.mpl_connect('button_press_event', on_mouse_click)
            print("Connected mouse events")

        else:
            print("Cursor is disabled or timestamp is not used")
            # Remove cursor elements if cursor is disabled or timestamp is not used
            if hasattr(self, 'vline') and self.vline in self.ax.lines:
                self.vline.remove()
                self.vline = None
                print("Removed main vline")
            if hasattr(self, 'markers'):
                for marker in self.markers:
                    if marker in self.ax.lines:
                        marker.remove()
                    if hasattr(marker, 'vline') and marker.vline in self.ax.lines:
                        marker.vline.remove()
                self.markers = []
                print("Removed markers and their vlines")
            if hasattr(self, 'text') and self.text in self.ax.texts:
                self.text.remove()
                self.text = None
                print("Removed text annotation")
            
            # Disconnect event handlers
            if hasattr(self, '_cid_motion'):
                self.fig.canvas.mpl_disconnect(self._cid_motion)
                del self._cid_motion
            if hasattr(self, '_cid_click'):
                self.fig.canvas.mpl_disconnect(self._cid_click)
                del self._cid_click
            print("Disconnected mouse events")

        self.canvas.draw()
        print("Canvas drawn")

        
    def display_selected_columns(self):
        print(f"Displaying - X-axis: {self.x_column}, Selected columns: {self.selected_columns}")  # 디버그 출력
        
        if self.df is not None and self.x_column and self.selected_columns:
            columns_to_display = [self.x_column] + self.selected_columns
            
            # Select only existing columns
            existing_columns = [col for col in columns_to_display if col in self.df.columns]
            
            if not existing_columns:
                print("No valid columns selected")
                return
            
            selected_data = self.df[existing_columns].copy()
            
            for col in existing_columns:
                if pd.api.types.is_numeric_dtype(selected_data[col]):
                    selected_data[col] = selected_data[col].apply(lambda x: f"{x:.3f}" if pd.notnull(x) else "")
                elif pd.api.types.is_datetime64_any_dtype(selected_data[col]):
                    selected_data[col] = selected_data[col].dt.strftime('%Y-%m-%d %H:%M:%S.%f')
                else:
                    selected_data[col] = selected_data[col].astype(str)

            self.update_data_table(selected_data)

            # Bind click event
            self.data_table.bind("<ButtonRelease-1>", self.on_table_click)
            
            # Bind selection event
            self.data_table.bind("<<TreeviewSelect>>", self.on_table_select)

    def on_table_select(self, event):
        selected_items = self.data_table.selection()
        if selected_items:
            item = selected_items[0]
            index = self.data_table.index(item)
            if 'timestamp' in self.df.columns:
                timestamp = self.df['timestamp'].iloc[index]
                self.update_cursor(timestamp)
                self.canvas.draw()

    def update_data_table(self, data):
        # Clear existing table
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        
        # Create new tree
        self.data_table = ttk.Treeview(self.table_frame, selectmode="extended")
        
        # Vertical scrollbar
        vsb = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.data_table.yview)
        vsb.pack(side='right', fill='y')
        
        # Horizontal scrollbar
        hsb = ttk.Scrollbar(self.table_frame, orient="horizontal", command=self.data_table.xview)
        hsb.pack(side='bottom', fill='x')
        
        # Configure the treeview
        self.data_table.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.data_table.pack(expand=True, fill=tk.BOTH)

        # Set up columns
        self.data_table['columns'] = list(data.columns)
        self.data_table['show'] = 'headings'
    
        for col in data.columns:
            self.data_table.heading(col, text=col, anchor='w')
            self.data_table.column(col, anchor='w', stretch=tk.NO)

        # Insert data
        for i, row in data.iterrows():
            self.data_table.insert('', 'end', values=list(row))
        
        # Adjust column widths after inserting data
        for col in data.columns:
            self.data_table.column(col, width=self.get_column_width(self.data_table, col))

        # Bind click event
        self.data_table.bind("<ButtonRelease-1>", self.on_table_click)

    def get_column_width(self, tree, col):
        header_width = len(str(col)) * 7
        max_data_width = max([len(str(tree.set(child, col))) * 7 for child in tree.get_children('')], default=0)
        return max(header_width, max_data_width, tree.column(col)['width'])

    def on_table_click(self, event):
        if not self.cursor_enabled:
            return

        item = self.data_table.identify('item', event.x, event.y)
        if item:
            index = self.data_table.index(item)
            if 'timestamp' in self.df.columns:
                timestamp = self.df['timestamp'].iloc[index]
                self.update_cursor(timestamp)
                self.canvas.draw()

    def on_graph_click(self, event):
        if event.inaxes == self.ax:
            if event.button == 1:  # Left click
                self.lock_cursor(event.xdata)
            elif event.button == 3:  # Right click
                self.unlock_cursor()

    def toggle_cursor_lock(self, event=None):
        if self.cursor_locked:
            self.unlock_cursor()
        else:
            self.lock_cursor()

    def lock_cursor(self, x):
        if x is not None:
            self.cursor_locked = True
            self.update_cursor(x)
            print(f"Cursor locked at x={x}")
        else:
            print("Cannot lock cursor: x is None")

    def unlock_cursor(self):
        self.cursor_locked = False
        print("Cursor unlocked")

    def update_cursor(self, x):
        if not self.cursor_enabled or not self.use_timestamp.get() or self.df is None:
            return
        
        # x가 None이면 업데이트하지 않음
        if x is None:
            return
        
        # 이전 위치와의 차이가 매우 작으면 업데이트하지 않음
        if self.last_cursor_x is not None and abs(self.last_cursor_x - x) < 1e-6:
            return
        
        self.last_cursor_x = x
        
        print(f"Updating cursor at x={x}")
        
        if self.vline:
            self.vline.set_xdata([x, x])
            print(f"Updated main vline to x={x}")
        
        closest_index = np.searchsorted(self.df[self.x_column].values, x)
        
        for column, marker in zip(self.selected_columns, self.markers):
            if column in self.df.columns:
                y = self.df[column].iloc[closest_index]
                marker.set_data([x], [y])
                marker.vline.set_xdata([x, x])
                
                # if hasattr(marker, 'vline'):
                    
                print(f"Updated marker and vline for {column} to ({x}, {y})")
        
        # Prepare the text to display
        text_lines = [f'Timestamp: {x:.3f}']
        text_lines.extend([f'{column}: {self.df[column].iloc[closest_index]:.3f}' for column in self.selected_columns])
        
        if len(self.selected_columns) == 2:
            y_values = [self.df[column].iloc[closest_index] for column in self.selected_columns]
            error = abs(y_values[0] - y_values[1])
            text_lines.append(f'Error: {error:.3f}')
        
        if self.text:
            self.text.set_text('\n'.join(text_lines))
            print("Updated text annotation")
        
        self.canvas.draw()
        print("Canvas updated")
        
        self.select_table_row(closest_index)

    def select_table_row(self, index):
        if hasattr(self, 'data_table'):
            children = self.data_table.get_children()
            if 0 <= index < len(children):
                self.data_table.selection_clear()
                iid = children[index]
                self.data_table.see(iid)
                self.data_table.selection_set(iid)

    # def convert_ulog(self, file_path=None):
    #     if file_path is None:
    #         file_path = filedialog.askopenfilename(filetypes=[("ULog files", "*.ulg")])
        
    #     if file_path:
    #         output_dir = os.path.dirname(file_path)
    #         command = f"ulog2csv -o {output_dir} {file_path}"
            
    #         def run_conversion():
    #             try:
    #                 subprocess.run(command, shell=True, check=True)
    #                 messagebox.showinfo("Conversion Complete", "ULog file has been converted to CSV.")
    #                 self.select_folder()  # Refresh the file list
    #             except subprocess.CalledProcessError:
    #                 messagebox.showerror("Conversion Error", "Failed to convert ULog file.")

    #         threading.Thread(target=run_conversion).start()
    def convert_ulog(self, file_path=None):
        if file_path is None:
            file_path = filedialog.askopenfilename(filetypes=[("ULog files", "*.ulg")])
        
        if file_path:
            base_dir = os.path.dirname(file_path)
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            
            new_folder_path = os.path.join(base_dir, file_name)
            os.makedirs(new_folder_path, exist_ok=True)
            
            csv_folder_path = os.path.join(new_folder_path, 'csv')
            os.makedirs(csv_folder_path, exist_ok=True)
            
            def run_conversion():
                try:
                    ulog = ULog(file_path)
                    
                    # # ulog_info
                    # with open(os.path.join(new_folder_path, 'ulog_info.txt'), 'w') as f:
                    #     f.write(f"File: {file_path}\n")
                    #     start_time = datetime.fromtimestamp(ulog.start_timestamp)
                    #     f.write(f"Logging start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    #     duration = timedelta(seconds=int(ulog.last_timestamp - ulog.start_timestamp))
                    #     f.write(f"Duration: {duration}\n")
                        
                    #     # Dropouts
                    #     if hasattr(ulog, 'dropouts') and ulog.dropouts:
                    #         dropout_durations = [dropout.duration for dropout in ulog.dropouts]
                    #         total_duration = sum(dropout_durations)
                    #         max_duration = max(dropout_durations)
                    #         mean_duration = total_duration / len(ulog.dropouts)
                    #         f.write(f"Dropouts: count: {len(ulog.dropouts)}, total duration: {total_duration:.1f} s, "
                    #                 f"max: {max_duration*1000:.0f} ms, mean: {mean_duration*1000:.0f} ms\n")
                        
                    #     # Info Messages
                    #     f.write("Info Messages:\n")
                    #     for key, value in ulog.msg_info_dict.items():
                    #         f.write(f" {key}: {value}\n")
                        
                    #     # Info Multiple Messages
                    #     if hasattr(ulog, 'msg_info_multiple_dict'):
                    #         f.write("Info Multiple Messages:\n")
                    #         for key, value in ulog.msg_info_multiple_dict.items():
                    #             f.write(f" {key}: {value}\n")
                        
                    #     # Data Messages
                    #     f.write("\nName (multi id)    number of data points\n")
                    #     for d in ulog.data_list:
                    #         num_data_points = len(d.data['timestamp'])
                    #         f.write(f" {d.name} ({d.multi_id})".ljust(30) +
                    #                 f"{num_data_points:8d}\n")
                    
                    # # messages
                    # with open(os.path.join(new_folder_path, 'messages.txt'), 'w') as f:
                    #     for msg in ulog.data_list:
                    #         f.write(f"{msg.name}: {msg.multi_id}\n")
                    
                    # params를 CSV로 저장
                    params_csv_path = os.path.join(new_folder_path, 'params.csv')
                    with open(params_csv_path, 'w', newline='') as csvfile:
                        csv_writer = csv.writer(csvfile)
                        csv_writer.writerow(['Parameter', 'Value'])  # CSV 헤더
                        for param_name, param_value in ulog.initial_parameters.items():
                            csv_writer.writerow([param_name, param_value])
                    
                    # CSV 파일 변환
                    convert_ulog2csv(
                        ulog_file_name=file_path,
                        output=csv_folder_path,
                        delimiter=',',
                        time_s=None,
                        time_e=None,
                        messages='',
                    )
                    
                    messagebox.showinfo("Conversion Complete", f"ULog file has been converted.\nOutput folder: {new_folder_path}")
                    self.select_folder()  # Refresh the file list
                except Exception as e:
                    messagebox.showerror("Conversion Error", f"Failed to convert ULog file: {str(e)}")

            threading.Thread(target=run_conversion).start()
 
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.quit()
            self.root.destroy()

    def update_bg_csv_combobox(self):
        self.bg_csv_combobox['values'] = self.all_csv_files
        if self.all_csv_files:
            self.bg_csv_combobox.set(self.all_csv_files[0])
            self.update_bg_data_combobox()

    def update_bg_data_combobox(self, event=None):
        selected_csv = self.bg_csv_combobox.get()
        if selected_csv:
            df = pd.read_csv(os.path.join(self.folder_path, selected_csv))
            self.bg_data_combobox['values'] = df.columns.tolist()
            if df.columns.tolist():
                self.bg_data_combobox.set(df.columns[0])

    def toggle_background(self):
        if self.background_applied:
            self.remove_background()
        else:
            self.apply_background()
        
        # 버튼 텍스트 업데이트를 여기서 직접 처리
        self.bg_apply_button.config(text="Remove Background" if self.background_applied else "Apply Background")

    def apply_background(self):
        selected_csv = self.bg_csv_combobox.get()
        selected_data = self.bg_data_combobox.get()
        if selected_csv and selected_data:
            try:
                bg_df = pd.read_csv(os.path.join(self.folder_path, selected_csv))
                if selected_data in bg_df.columns and 'timestamp' in bg_df.columns:
                    self.bg_data = bg_df[['timestamp', selected_data]].copy()
                    self.bg_data['timestamp'] = self.bg_data['timestamp'] * 1e-6
                    
                    # 값이 변하는 지점 찾기
                    self.bg_data['value_change'] = self.bg_data[selected_data].diff() != 0
                    self.bg_data = self.bg_data[self.bg_data['value_change'] | (self.bg_data.index == 0)]
                    
                    # 값이 변하는 지점마다 카운트 증가
                    self.bg_data['change_count'] = range(len(self.bg_data))
                    
                    # 색상 할당
                    self.bg_data['color'] = self.bg_data['change_count'].apply(self.get_color_for_value)
                    
                    self.background_applied = True
                    self.bg_column = selected_data
                    self.plot_selected_columns()  # 여기서 그래프를 다시 그립니다.
                    # 버튼 텍스트 업데이트
                    self.bg_apply_button.config(text="Remove Background")
                else:
                    messagebox.showwarning("Warning", "Selected data column or timestamp not found in the CSV file.")
                    self.reset_background()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to apply background: {str(e)}")
                self.reset_background()
        else:
            messagebox.showwarning("Warning", "Please select both CSV file and data column for background.")
            self.reset_background()

    def remove_background(self):
        self.background_applied = False
        self.bg_data = None
        self.plot_selected_columns()  # 배경을 제거한 후 그래프를 다시 그립니다.

    def get_color_for_value(self, value):
        colors = [
            '#FFFF00',  # 노랑
            '#7FFF00',  # 연두
            '#00FF00',  # 초록
            '#00FF7F',  # 청록
            '#00FFFF',  # 하늘
            '#007FFF',  # 파랑
            '#0000FF',  # 남색
            '#7F00FF'   # 보라
            '#FF0000',  # 빨강
            '#FF7F00',  # 주황
        ]
        return colors[int(value) % len(colors)]

    def reset_background(self):
        self.background_applied = False
        self.bg_data = None
        self.bg_apply_button.config(text="Apply Background")

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVViewerApp(root)
    root.mainloop()