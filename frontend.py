import base64


def get_image(path):
    file = open(path, 'rb')
    data_uri = str(base64.b64encode(file.read()), 'utf-8')
    file.close()
    return data_uri


def get_index(is_index=True):
    html = ''
    if is_index:
        html += '<h2 style=\"text-align: center\">输入URL或歌词</h2>'
    html += '<input type="radio" checked="checked" value="1" name="ra" style="margin-left:40%"/>' \
            '<span>罗马音</span>'
    html += '<input type="radio" value="2" name="ra" /><span>汉语拼音</span>'
    html += '<input type="radio" value="3" name="ra" /><span>中文谐音</span>'
    html += '<br/>'
    html += '<button id="transBtn" style="margin-left:35%;height: 10%;width: 30%;' \
            'line-height:40px;background-color:rgb(51,133,255); margin-top:20px" ' \
            'onclick="this.disabled=true;this.innerHTML=\'请等待...\';search()">注音</button>'
    html += '<textarea id="keyword" ' \
            'style="margin-left: 25%;width:50%;height: 400px;line-height:40px;font-size:22px;margin-top:10px"></textarea>'

    html += '<script>'
    html += 'function search() \
        {	\
            var temp = document.getElementsByName("ra");\
            var resultType = 0;\
            for (var i = 0, length = temp.length; i < length; i++) {\
                if (temp[i].checked) {\
                    resultType = i + 1;\
                    break;\
                }\
            };\
            var BtnDom = document.getElementById("transBtn");\
            var inputDom = document.getElementById(\"keyword\");\
            window.location.href=\'/type=\'+ resultType + \'&translate?url=\' + encodeURI(inputDom.value);\
        }'
    html += '</script>'
    return html