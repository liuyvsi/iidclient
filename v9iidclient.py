#!/usr/bin/env python
import npyscreen, curses
import requests
import json

class LoginRequest:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class TokenResponse:
    def __init__(self, message, status, data):
        self.message = message
        self.status = status
        self.data = data

class TokenData:
    def __init__(self, token):
        self.token = token

class MyTestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.token_data = "no token"
        self.ip_address = "172.17.0.3"
        self.port_number = 8080    
        # When Application starts, set up the Forms that will be used.
        # These two forms are persistent between each edit.
        self.addForm("MAIN",       MainForm, name="主菜单", color="IMPORTANT",)
        # This one will be re-created each time it is edited.
        self.addFormClass("TOKEN",     tokenForm, name="令牌申请", color="IMPORTANT",  )
        self.addFormClass("TEMPLATEREG",     tmplateregForm, name="模板注册", color="IMPORTANT",  )
        self.addFormClass("TEMPLATEBROWSE",     tmplatebrowseForm, name="模板查询", color="IMPORTANT",  )
        self.addFormClass("IIDREG",     iidregForm, name="标识注册", color="IMPORTANT",  )
        self.addFormClass("IIDBROWSE",     iidbrowseForm, name="标识查询", color="IMPORTANT",  )
 
        
         
    def onCleanExit(self):

        npyscreen.notify_wait("Goodbye!")
    
    def change_form(self, name):
        # Switch forms.  NB. Do *not* call the .edit() method directly (which 
        # would lead to a memory leak and ultimately a recursion error).
        # Instead, use the method .switchForm to change forms.
        self.switchForm(name)
        
        # By default the application keeps track of every form visited.
        # There's no harm in this, but we don't need it so:        
        self.resetHistory()
    
class MainForm(npyscreen.FormWithMenus):
   
    def create(self):
      
        self.how_exited_handers[npyscreen.wgwidget.EXITED_ESCAPE]  = self.exit_application    
    
       
        # The menus are created here.

        self.m1 = self.add_menu(name="系统", shortcut="^M")
        self.m1.addItemsFromList([
            ("版本号", self.whenDisplayText, None, None, ("版本号：V0.02",)),
            ("退出", self.exit_application, "é"),
        ])
        self.add(npyscreen.ButtonPress, name="令牌申请", when_pressed_function=self.change_token)
        self.add(npyscreen.ButtonPress, name="模板注册", when_pressed_function=self.change_template_reg)
        self.add(npyscreen.ButtonPress, name="模板查询", when_pressed_function=self.change_template_browse)
        self.add(npyscreen.ButtonPress, name="标识注册", when_pressed_function=self.change_iid_reg)
        self.add(npyscreen.ButtonPress, name="标识查询", when_pressed_function=self.change_iid_browse)
        self.add(npyscreen.ButtonPress, name="退出", when_pressed_function=self.exit_application)

    def custom_action(self):
        npyscreen.notify_confirm("Custom button pressed!")
        
    def another_action(self):
        npyscreen.notify_confirm("Another button pressed!")
        
    def on_ok(self):
        self.exit_application()

    def change_token(self):
        self.parentApp.change_form("TOKEN")

    def change_template_reg(self):
        self.parentApp.change_form("TEMPLATEREG")  

    def change_template_browse(self):
        self.parentApp.change_form("TEMPLATEBROWSE")  
    
    def change_iid_reg(self):
        self.parentApp.change_form("IIDREG")  

    def change_iid_browse(self):
        self.parentApp.change_form("IIDBROWSE")  
    
    def whenDisplayText(self, argument):
       npyscreen.notify_confirm(argument)

    def whenJustBeep(self):
        curses.beep()

    def exit_application(self):
        curses.beep()
        self.parentApp.setNextForm(None)
        self.editing = False
        self.parentApp.switchFormNow()

class tokenForm(npyscreen.ActionForm):
    def create(self):
        self.showlist=[ self.parentApp.token_data,
                        "",
                        "",
                        "",]
        self.add(npyscreen.TitleText, name = "Text:", value= "令牌测试" )
        self.un =self.add(npyscreen.TitleText, name="username:", rely=3)
        self.pd =self.add(npyscreen.TitlePassword, name="password:", rely=4)
             # 添加 OK 按钮
        self.add(npyscreen.ButtonPress, name="确认", when_pressed_function=self.get_token)
        self.show = self.add(npyscreen.MultiLine,
                            max_height=20,
                            name='List of Values',
                            values= self.showlist,
                            slow_scroll=False)
        

   
    
    def update_values(self, new_values):
        self.showlist=new_values
        self.show.values = self.showlist
        # Refresh the display
        self.show.display()

    def get_token(self):
        username = self.un.value
        password = self.pd.value
        login_request = LoginRequest(username, password)

        # Simulate the POST request for login
        tmp_str = f"http://{self.parentApp.ip_address}:{self.parentApp.port_number}/identity/token"
        login_response = requests.post(tmp_str, json=login_request.__dict__)
        token_response = login_response.json()

        if token_response["status"] == 1:
            self.parentApp.token_data =token_response["data"]["token"]
            formatted_list = [f"成功", f"令牌是 {self.parentApp.token_data}"]
            self.update_values(formatted_list)
        else:   
            formatted_list = [f"失败", f"Login failed: {token_response['message']}"]
            self.update_values(formatted_list)


    def on_ok(self):
        # change to 主菜单 if the OK button is pressed.
        self.parentApp.change_form("MAIN")   

class tmplateregForm(npyscreen.ActionForm):
    def create(self):
        self.new_data = {
            "prefix": "",
            "version":  "",
            "industryCategory":  "",
            "industrySpecific": "",
            "industryTrade":  "",
            "industrySubclass":  "",
            "type":  "",  # Assuming type is an integer
            "description":  "",
            "items":[]
        }


        self.prefix = self.add(npyscreen.TitleText, name="prefix", value="88.529", max_width=40)
        self.version = self.add(npyscreen.TitleText, name="version", value="1.0.0", max_width=40)
        self.industry_category = self.add(npyscreen.TitleText, name="industryCategory", value="A", max_width=40)
        self.industry_specific = self.add(npyscreen.TitleText, name="industrySpecific", value="01", max_width=40)
        self.industry_trade = self.add(npyscreen.TitleText, name="industryTrade", value="011", max_width=40)
        self.industry_subclass = self.add(npyscreen.TitleText, name="industrySubclass", value="0111", max_width=40)
        self.type = self.add(npyscreen.TitleText, name="type", value="1", max_width=40)
        self.description = self.add(npyscreen.TitleText, name="description", value="English display ok", max_width=40)

        # 添加确认按钮
        self.confirm_button = self.add(npyscreen.ButtonPress, name="修改模板", when_pressed_function=self.newtemplate_handle)
        self.add(npyscreen.FixedText, name="Text:", value="————————       字段   ———————————————", editable=False)
        self.name = self.add(npyscreen.TitleText, name="Name", value="", max_width=40)
        self.id_type = self.add(npyscreen.TitleText, name="ID Type", value="", max_width=40)
        self.id_index = self.add(npyscreen.TitleText, name="ID Index", value="3000", max_width=40)
        self.min_length = self.add(npyscreen.TitleText, name="Min Length", value="1", max_width=40)
        self.max_length = self.add(npyscreen.TitleText, name="Max Length", value="10", max_width=40)

        self.required = self.add(npyscreen.Checkbox, name="Required", value=False)

        self.newfield_button = self.add(npyscreen.ButtonPress, name="新增字段", when_pressed_function=self.newfield_handle)
        self.add(npyscreen.FixedText, name="Text:", value="——————————————————————————————————————", editable=False)
        self.send_button = self.add(npyscreen.ButtonPress, name="回车发送申请", when_pressed_function=self.send_handle)
       
        self.show = self.add(npyscreen.MultiLineEdit, name="Answer:", value=json.dumps(self.new_data,indent=4), scroll_exit=True)

    def newtemplate_handle(self):
        # Handle the button press, you can access the values using self.<control_name>.value
        original_items = self.new_data["items"]
        self.new_data = {
            "prefix": self.prefix.value,
            "version": self.version.value,
            "industryCategory": self.industry_category.value,
            "industrySpecific": self.industry_specific.value,
            "industryTrade": self.industry_trade.value,
            "industrySubclass": self.industry_subclass.value,
            "type": int(self.type.value),  # Assuming type is an integer
            "description": self.description.value,
            "items":original_items
        }
        self.show.value = json.dumps(self.new_data,indent=4)
        self.show.display()

    def newfield_handle(self):
        data = {
            "name": self.name.value,
            "idType": self.id_type.value,
            "idIndex": self.id_index.value,
            "metadata": {
                "type":  "String",
                "minLength": int(self.min_length.value) if self.min_length.value else None,
                "maxLength": int(self.max_length.value) if self.max_length.value else None
            },
            "required": self.required.value
        }
        self.new_data["items"].append(data)
        self.show.value = json.dumps(self.new_data, indent=4)
        self.show.display()
    
    def send_handle(self):
        try:
            tmpdata = self.new_data
            headers = {"Authorization": f"Bearer {self.parentApp.token_data}"}
            url = f"http://{self.parentApp.ip_address}:{self.parentApp.port_number}/snms/template_creat"
            response = requests.post(url,headers=headers, json=tmpdata)
            
            # 检查响应状态码
            response.raise_for_status()


            # 尝试解析为JSON
            newtemplate_response = response.json()

            self.show.value = json.dumps(newtemplate_response, indent=4)
        #    with open('output.json', 'w') as f:
                # 将JSON对象转换为字符串，然后写入到文件中
        #        json.dump(tmpdata, f)
            self.show.display()

        except requests.exceptions.RequestException as e:
            # 处理请求异常
            self.show.value = f"Error in request: {e}\n" + json.dumps(self.new_data, indent=4)
            self.show.display()
        
        except json.JSONDecodeError as e:
            # 处理JSON解析异常
            self.show.value = f"Error decoding JSON: {e}"
            self.show.display()

    def on_ok(self):
            # change to 主菜单 if the OK button is pressed.
            self.parentApp.change_form("MAIN")

class tmplatebrowseForm(npyscreen.ActionForm):
    def create(self):
        
        self.pre = self.add(npyscreen.TitleText, name="prefix:88.529",value="/",max_width=40)
        self.ver = self.add(npyscreen.TitleText, name="version",max_width=40)
        # 添加 确认 按钮
        self.confirm_button = self.add(npyscreen.ButtonPress, name="确认", when_pressed_function=self.requir_handle,rely=5)
        self.add(npyscreen.FixedText, name="Text:", value="——————————————————————————————————————",rely=6,editable = False)
        longtxt = "*                 \n" * 20
        self.show = self.add(npyscreen.MultiLineEdit, name ="Answer:",value=longtxt,scroll_exit=True)
    
    def beforeEditing(self):
        self.display()
#        self.pre.edit()

    def on_ok(self):
        # change to 主菜单 if the OK button is pressed.
        self.parentApp.change_form("MAIN")

    def requir_handle(self):
   
        headers = {"Authorization": f"Bearer {self.parentApp.token_data}"}
        req_str1 = f"http://{self.parentApp.ip_address}:{self.parentApp.port_number}/snms/template?prefix=88.529{self.pre.value}&version={self.ver.value}"
#debug        req_str1 = f"http://172.17.0.3:8080/snms/template?prefix=888889&version=7788"
    #    identity_response = requests.get(req_str1, headers=headers).json()
        identity_response = requests.get(req_str1, headers=headers).json()
        
        self.show.value = json.dumps(identity_response, indent=4)


        self.show.display()

class iidregForm(npyscreen.ActionForm):
    def create(self):
        self.add(npyscreen.TitleText, name = "Text:", value= "标识注册测试" )

    def on_ok(self):
        # change to 主菜单 if the OK button is pressed.
        self.parentApp.change_form("MAIN")

class iidbrowseForm(npyscreen.ActionForm):
    def create(self):
        
        self.ha = self.add(npyscreen.MultiLineEdit, name="handle", max_height=2,rely=2)
        self.add(npyscreen.FixedText, name="Text:", value="handle: 88.529/",rely=1,editable = False)
             # 添加 OK 按钮
        self.confirm_button = self.add(npyscreen.ButtonPress, name="确认", when_pressed_function=self.requir_handle,rely=5)
        self.add(npyscreen.FixedText, name="Text:", value="——————————————————————————————————————",rely=6,editable = False)
        longtxt = "*                 \n" * 20
        self.show = self.add(npyscreen.MultiLineEdit, name ="Answer:",value=longtxt,scroll_exit=True,editable = False)


    
    def beforeEditing(self):
        self.display()
        self.ha.edit()



    def on_ok(self):
        # change to 主菜单 if the OK button is pressed.
        self.parentApp.change_form("MAIN")

    def requir_handle(self):
        headers = {"Authorization": f"Bearer {self.parentApp.token_data}"}
        req_str = f"http://{self.parentApp.ip_address}:{self.parentApp.port_number}/identityv2/data/detail?handle=88.529/{self.ha}"
        identity_response = requests.get(req_str, headers=headers).json()
        self.show.value = json.dumps(identity_response, indent=4)
        self.show.display()

def main():
    TA = MyTestApp()
    TA.run()


if __name__ == '__main__':
    main()