from cv2 import imread, imwrite, resize, INTER_AREA, IMREAD_UNCHANGED
import os, re

from database.dao_image import *
from database.dao_setting import *
from database.dao_icon_color import *

class SettingController(object):
    def __init__(self, image_model, setting_model, icon_model):
        super().__init__()

        self._image_model = image_model
        self._setting_model = setting_model
        self._icon_model = icon_model
        self.load()

    def load(self):
        if(len(self.get_images()) == 0):
            self._image_model.add_all_image({i[0]: list(i) for i in getImageAll()})
        if(len(self.get_settings()) == 0):
            self._setting_model.add_all_setting({i[0]: list(i) for i in getSettingAll()})
        if len(self.get_icons()) == 0:
            self._icon_model.add_all_icon({i[0]: list(i) for i in getIconColorAll()})
    
    def get_images(self):
        return self._image_model.get_image()
    
    def get_settings(self):
        return self._setting_model.get_setting()
    
    def get_icons(self):
        return self._icon_model.get_icon()

    def add_image_to_database(self, name):
        if len(self.get_images()) == 10:
            return None
        if len(self.get_images()) == 0:
            new_id = 100
        else:
            new_id = list(self.get_images().keys())[-1] + 1

        addImage(new_id, name, 0)
        self.get_images()[new_id] = [new_id, name, 3]
        return new_id
    
    def get_theme(self):
        for values in self.get_settings().values():
            if values[7] == 1:
                return values
            
    def get_icon_from_id_color(self, id):
        return self.get_icons()[id]
    
    def get_active_image(self):
        for values in self.get_images().values():
            if values[2] != 3:
                return values[2]
    
    def change_accent(self, color):
        with open('Qss/scss/_styles.scss', 'r') as file:
            css_content = file.read()

        for variable in ['COLOR_ACCENT_1', 'COLOR_ACCENT_2', 'COLOR_ACCENT_3', 'COLOR_ACCENT_4']:
            sub_css_content = re.sub(rf'\${re.escape(variable)}\b', color, css_content)
            css_content = sub_css_content

        with open('Qss/scss/_styles2.scss', 'w') as file:
            file.write(sub_css_content)

    def update_setting(self, bg, accent, widget, icon):
        color_pattern = re.compile("^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")
        if not color_pattern.match(bg[0]):
            bg_temp = int(bg[0])
            for values in self.get_images().values():
                if values[2] != 3:
                    updateImage(values[0], 3)
                    self.get_images()[values[0]][2] = 3
                    break
            updateImage(bg_temp, bg[1])
            self.get_images()[bg_temp][2] = bg[1]
            bg_temp = f"img/{bg[0]}_bg.png"

        else:
            bg_temp = bg[0]
            for values in self.get_images().values():
                if values[2] != 3:
                    updateImage(values[0], 3)
                    self.get_images()[values[0]][2] = 3
                    break

        updateSetting(bg_temp, accent, widget, icon)
        updateStatus(1, 0)
        self.get_settings()[2] = [2, bg_temp, "img/resource/logo3.png", "img/resource/main3.png", accent, widget, icon, 1]
        self.get_settings()[1][7] = 0
        self.change_accent(accent)


    def delete_image(self, id):
        id = int(id)
        deleteImage(id)
        del self.get_images()[id]
        paths = [f"img/{id}_bg.png", f"img/{id}_demo.png", f"img/{id}.png"]
        for path in paths:
            try:
                os.remove(path) 
                print(f"Đã xóa hình ảnh từ đường dẫn '{path}'.")
            except FileNotFoundError:
                print(f"Hình ảnh từ đường dẫn '{path}' không tồn tại.")
            except Exception as e:
                print(f"Lỗi khi xóa hình ảnh từ đường dẫn '{path}': {e}")


    def reset_setting(self):
        updateStatus(2, 0)
        updateStatus(1, 1)
        self.get_settings()[2][7] = 0
        self.get_settings()[1][7] = 1

    def make_noti_icon(self, color):
        color = color.replace("#", "")
        image = imread("Qss/icons/" + color + "/font_awesome/solid/bell.png", IMREAD_UNCHANGED)
        original_height, original_width = image.shape[:2]
        scale_x = 25 / original_width
        scale_y = 25 / original_height
        scale_factor = max(scale_x, scale_y)
        scaled_image = resize(image, None, fx=scale_factor, fy=scale_factor, interpolation=INTER_AREA)
        output_path = "img/resource/bell.png"
        imwrite(output_path, scaled_image)

    def read_and_save_image(self, input_image_path, output_image_path):
        image = imread(input_image_path, IMREAD_UNCHANGED)
        imwrite(output_image_path, image)

    def scale_image(self, id, target_width, target_height, index, demo=None):
        end_path = "_demo.png" if demo else "_bg.png"
        id_image_demo = id if demo else None  

        image = imread(f"img/{id}.png", IMREAD_UNCHANGED)
        if image is None:
            print(f"Không tìm thấy ảnh tại đường dẫn: img/{id}.png.")
            return None

        # Lấy kích thước của ảnh gốc
        original_height, original_width = image.shape[:2]

        # Xác định tỷ lệ co giãn
        scale_x = target_width / original_width
        scale_y = target_height / original_height

        if index == 0:
            scaled_image = resize(image, None, fx=scale_x, fy=scale_y, interpolation=INTER_AREA)
            output_path = "img/" + id + end_path
            imwrite(output_path, scaled_image)
            return output_path, id_image_demo
        
        elif index == 2:
            scale_factor = min(scale_x, scale_y)

        else:
            scale_factor = max(scale_x, scale_y)

        scaled_image = resize(image, None, fx=scale_factor, fy=scale_factor, interpolation=INTER_AREA)
        output_path = "img/" + id + end_path
        imwrite(output_path, scaled_image)
        return output_path, id_image_demo
