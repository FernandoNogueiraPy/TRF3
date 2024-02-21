import asyncio
import requests
import re
import io









class RequestsScrapper():        
    

    def __init__(self,url:str) -> None:
        self.url = url
        self.session = requests.Session()

    def controler_class(self):
        document = self.get_document()

        document_str = document.decode('utf-8')  # Decode bytes to string
        matches = self.regex_trf3(document_str)  # Pass the string to the function


        for match in matches:
            self.register_document(match)

    def get_document(self):
        response = self.session.get(self.url)
        return response.content

    def get_document_as_io(self,response:requests.models.Response):
        with io.BytesIO(response.content) as file:
            return file
        
    def regex_trf3(self,document:str):   

        regex = r"(\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})"
        matches = re.findall(regex, document, re.MULTILINE)
        return matches

    def register_document(self,id:str):
        
        with open(f"controler_register.txt", "a") as file:
            file.write(f"{id}\n")
        
        print(f"Documento {id} registrado com sucesso")






url =  'https://asana-user-private-us-east-1.s3.us-east-1.amazonaws.com/assets/1205206908797044/1206635303326821/48cbb856821410ff08c435b21b129496?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAV34L4ZY4AIPYMG4T%2F20240220%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240220T195848Z&X-Amz-Expires=120&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEEsaCXVzLWVhc3QtMSJGMEQCIHsMMema6LjxrqwFQ4hH1OYis4lSULrWNshQpZLv0j7KAiBxLbWqBqa54e%2BTOm0VcJbkbwXIEi%2BVkGwe6pf%2BI6qOsyqwBQg0EAAaDDQwMzQ4MzQ0Njg0MCIMkiTDU5eVbVHBv3hcKo0FbJEKUcOPR%2BsO1hSgCS9%2F9WO%2BNfKfc3Kzi2o2myK3Hus%2BftI%2FaWOlMGsMrQ0c5AfTRRSlHOV4Qsx8gIDNKAxpnVsrSfJLAM5UVS9l0LxFGvNhc3jIsaOazyjwB0azbfQxqIotR4YOKZ8FtwBTrSbSh36IJQQSwacHd14u48ivKuGOEYiEfihVgTwwEoQ%2FwJZ5O0Ov6l5P2Nx9npzm6bPAI%2FiYulnouubaCDwCEEE9VvdOL0imvvXgxywP6AgoE7Purv1QF8n9QQQHd7QT5vSMNDWykweo8ysVrBnYAnbadGHBrMKjuNxUreOKy0bVLoloyTMUEvaQpABtn%2Bi9kHfGFm5OiEw66yvyaRpM3fm9J8aI%2FJFICNHiJGooP9zetAeg9QhJn1Wz6dNYEpbGnaesU3VKSOaXSdSHYi83X8ZReN9J8%2BkiNMkBPHROHVNqZduH0g0IA7nesME3GEW7S2oj5m3fbYx6hiKz3er7zXXxt5j2bRLxle%2BdpsKljOdh1LdUlu3d9QgJXVV4d12VkVU6qIbf2Yrpmt0rZMhcbLc84MWQGZXjOAXQjzlCjR1288m47Uwy0dw1F4Mu2rHC6Knjr3rGAZiH3TowkmM7MyVZcr3Mpj93JziNaW9BVL88qVMwANIoWrgJaOpRdrxXhfMgQRa954nquCm%2BcmSIdbJ6xetR8r0kQsZQN%2Fw1wC5SkYTj60afy8dnp1%2F4MwStc35V1DuBBI2aOQbnY38JbkuQyD9p4d2njSTZWRIX0Pa5Mpe%2FVLg%2BR945LViGJxfJTrhWDmQS6DJ41FT%2FsBJV7%2FpKe75%2BMRO%2Fpefo6XWXkJVtFDziqoA0KNoXtz2TjFY5x81n27Kfk0bIE%2BKcBizs5OEw%2B%2BPTrgY6sgHYMxpJSePi4gklour86g%2BELrmkfitzyGOG8yJ5rc%2FZEQQ2s11SO%2B3dwKi5oeMdstW7xqseunmPnbdAKMI5LkngLA8u8hO0o6b6OZm7ANZZwj4yStZUFWKl4GZhGO4XlziU7qcDnb4WBNvd%2FchvXlxCqJISTd0tOc93eLNuuQw6vvlI96RoN56WN0KmgfvS9%2FUNKdnINlPv3UwXhJvCw0XpOJxrhWdu5jv3olVYSXxO4UQ8&X-Amz-Signature=baeeea38fe0785aaf1c21e129c840959fcfe60c16acdcd936658af3a002fea71&X-Amz-SignedHeaders=host&x-id=GetObject#_=_'
