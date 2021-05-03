from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
import openpyxl as xl
import xml.etree.ElementTree as ET
import uuid
from . import dttype as dt
import requests
# Create your views here.
class index(View):
    def get(self, request):
        return render(request, 'myapp/index.html')

class upload(View):
    def get(self, request):
        return render(request, 'myapp/upload.html')
    
    def post(self, request):
        if request.FILES.get('excel_file'):
            excel_file = request.FILES.get('excel_file')
            print((excel_file))
            # tieude = mail.cleaned_data['title']
            # noidung = mail.cleaned_data['content']
            # email = mail.cleaned_data['email']
            # cc = mail.cleaned_data['email']
            # _file = request.FILES['_file']
            wb = xl.load_workbook(excel_file)
            sh = wb['Sheet1']
            m_row = sh.max_row
            last_line = 0
            data = {'Patient':{},'Encounter':{},'Observation':[]}
            for i in range(1,m_row+1):
                cell = sh.cell(row=i, column=4)
                if(cell.value):
                    tag = sh.cell(row=i, column=2)
                    if tag.value == 'HO_TEN':
                        data['Patient']['name'] = [cell.value]
                    elif tag.value == 'NGAY_SINH':
                        data['Patient']['birthDate'] = cell.value
                    elif tag.value == 'GIOI_TINH':
                        data['Patient']['gender'] = cell.value
                    elif tag.value == 'DIA_CHI':
                        data['Patient']['address'] = [{'address':cell.value}]
                    elif not tag.value:
                        tag_2 = sh.cell(row=i, column=3)
                        tag_2_content = tag_2.value.split('.')
                        if tag_2_content[0] == 'Patient':
                            if data['Patient'][tag_2_content[1]]:
                                data['Patient'][tag_2_content[1]].append({tag_2_content[1]:cell.value})
                                if len(tag_2_content) > 2:
                                    for i in range(2, len(tag_2_content)):
                                        data['Patient'][tag_2_content[1]][-1][tag_2_content[i].split('=')[0]] = tag_2_content[i].split('=')[1]
            id_system = ""
            root = ET.Element('Patient')
            tree = ET.ElementTree(root)
            root.set("xmlns","http://hl7.org/fhir")
            if data['Patient'].values():
                identifier = ET.SubElement(root, 'identifier')
                dt.identifier_type(identifier, 'urn:trinhcongminh', '12345', 'usual',{'codes': [{'system': 'http://terminology.hl7.org/CodeSystem/v2-0203', 'code': 'MR'}]})
                if data['Patient'].get('name'):
                    for value in data['Patient']['name']:
                        name = ET.SubElement(root, 'name')
                        dt.name_type(name, value)
                if data['Patient'].get('gender'):
                    gender = ET.SubElement(root, 'gender')
                    if data['Patient']['gender'] == 'Nam':
                        code = 'male'
                    elif data['Patient']['gender'] == 'Nu':
                        code = 'female'
                    gender.set('value', code)
                if data['Patient'].get('birthDate'):
                    birthDate = ET.SubElement(root, 'birthDate')
                    birthDate.set('value', data['Patient']['birthDate'])
                if data['Patient'].get('address'):
                    for value in data['Patient']['address']:
                        address = ET.SubElement(root,'address')
                        dt.address_type(address, value.get('address'),value.get('postalCode'),value.get('country'),value.get('use'),value.get('type'))
                if data['Patient'].get('contact'):
                    contact = ET.SubElement(root, 'contact')
            text = ET.tostring(root, encoding="us-ascii", method="xml", xml_declaration=None, default_namespace=None, short_empty_elements=True)
            # print(type(text.decode('utf-8')))
            # print(text.decode('utf-8'))
            x = requests.post("http://hapi.fhir.org/baseR4/Patient/", headers={'Content-type': 'application/xml'}, data=text.decode('utf-8'))                                                 
            print(x.status_code)
            print(x.content)
            print(x.content.decode('utf-8'))
            if x.status_code == 201:
                return render(request, 'myapp/index.html', {'message': 'Upload successful'})
            else: return render(request, 'myapp/index.html',{'message': 'Failed to create resource, please check your file!'})
        else: return render(request, 'myapp/index.html',{'message':'Please upload your file!'})

class search(View):
    def post(self, request):
        if request.POST:
            x = requests.get("http://hapi.fhir.org/baseR4/Patient?identifier=urn:trinhcongminh|" + request.POST['identifier'], headers={'Content-type': 'application/xml'})
            if x.status_code == 200 and 'entry' in x.content.decode('utf-8'):
                return render(request, 'myapp/index.html', {'message': 'Patient data existed'})
            else: 
                return render(request, 'myapp/index.html', {'message': 'Patient not found in database'})
        else:
            return render(request, 'myapp/index.html', {'message':'Please enter an identifier'})

class register(View):
    def get(self, request):
        return render(request, 'myapp/register.html')
    def post(self, request):
        if request.POST:
            patient = {}
            patient['name'] = request.POST['ho_ten']
            patient['gender'] = request.POST['gioi_tinh']
            patient['birthDate'] = request.POST['ngay_sinh']
            patient['address'] = [{'address': request.POST['dia_chi'], 'use': 'home'}, {'address': request.POST['noi_lam_viec'], 'use': 'work'}]
            patient['identifier'] =str(uuid.uuid4())
            print(type(patient['identifier']))
            print(patient)
            id_system = "urn:trinhcongminh"
            root = ET.Element('Patient')
            tree = ET.ElementTree(root)
            root.set("xmlns","http://hl7.org/fhir")
            if patient.values():
                if patient.get('identifier'):
                    identifier = ET.SubElement(root, 'identifier')
                    dt.identifier_type(identifier, id_system, patient['identifier'], 'usual',{'codes': [{'system': 'http://terminology.hl7.org/CodeSystem/v2-0203', 'code': 'MR'}]})
                if patient.get('name'):
                    # for value in patient.get('name'):
                    name = ET.SubElement(root, 'name')
                    dt.name_type(name, patient['name'])
                if patient.get('gender'):
                    gender = ET.SubElement(root, 'gender')
                    if patient['gender'] == 'Nam':
                        code = 'male'
                    elif patient['gender'] == 'Nu':
                        code = 'female'
                    gender.set('value', code)
                if patient.get('birthDate'):
                    birthDate = ET.SubElement(root, 'birthDate')
                    birthDate.set('value', patient['birthDate'])
                if patient.get('address'):
                    for value in patient['address']:
                        address = ET.SubElement(root,'address')
                        dt.address_type(address, value.get('address'),value.get('postalCode'),value.get('country'),value.get('use'),value.get('type'))
                if patient.get('contact'):
                    contact = ET.SubElement(root, 'contact')
            text = ET.tostring(root, encoding="us-ascii", method="xml", xml_declaration=None, default_namespace=None, short_empty_elements=True)
            # print(type(text.decode('utf-8')))
            # print(text.decode('utf-8'))
            x = requests.post("http://hapi.fhir.org/baseR4/Patient/", headers={'Content-type': 'application/xml'}, data=text.decode('utf-8'))
            return render(request, 'myapp/display.html', {'patient':patient})
        else: return HttpResponse("Please enter your information")
    