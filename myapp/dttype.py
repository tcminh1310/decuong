import xml.etree.ElementTree as ET

def identifier_type(resource, system, value, use="usual", _type=None, period=None, assigner=None):
    ET.SubElement(resource, 'use value=\"{}\"'.format(use))
    if _type:
        type_res = ET.SubElement(resource, 'type')
        codeable_concept(type_res, len(_type['codes']), _type)
    ET.SubElement(resource, 'system value=\"{}\"'.format(system))
    ET.SubElement(resource, 'value value=\"{:0>5}\"'.format(value))
    if period:
        period_res = ET.SubElement(resource, 'period')
        period_type(period_res, period)
    if assigner:
        assigner_res = ET.SubElement(resource, 'assigner')
        reference_type(assigner_res, assigner.reference, assigner._type, assigner_res.identifier)
    

def period_type(resource, start=None, end=None):
    if start:
        ET.SubElement(resource, 'start value=\"{}\"'.format(start))     
    if end:       
        ET.SubElement(resource, 'end value=\"{}\"'.format(end))


def reference_type(resource, reference, _type, identifier = None, display=None):
    ET.SubElement(resource, 'reference value=\"{}\"'.format(reference))
    ET.SubElement(resource, 'type value=\"{}\"'.format(_type))
    if identifier:    
        _identifier = ET.SubElement(resource, 'identifier')
        identifier_type(_identifier, identifier.get('system'), identifier.get('value'), identifier.get('use'), idetifier.get('type'), identifier.get('period'), identifier('assigner'))
    if display:
        ET.SubElement(resource, 'display value=\"{}\"'.format(display))

def name_type(resource, name, text=None, use=None):
    fam_name = name.split(' ')[0]
    given_name = ' '.join(name.split(' ')[1:])
    if not use:
        use = "official"
    ET.SubElement(resource, 'use value=\"{}\"'.format(use))
    if text:
        ET.SubElement(resource, 'text value=\"{}\"'.format(text))
    ET.SubElement(resource, 'family value=\"{}\"'.format(fam_name))
    ET.SubElement(resource, 'given value=\"{}\"'.format(given_name))
    

def address_type(resource, address, postalCode=None, country=None, use=None, type_=None):
    city = address.split(', ')[-1]
    district = address.split(', ')[-2]
    line = ' '.join(address.split(', ')[:-2])
    if not use:
        use = "home"
    if not type_:
        type_ = "both"
    if not postalCode:
        postalCode = "70000"
    if not country:
        country = "VietNam"
    ET.SubElement(resource, 'use value=\"{}\"'.format(use))
    ET.SubElement(resource, 'type value=\"{}\"'.format(type_))
    ET.SubElement(resource, 'line value=\"{}\"'.format(line))
    ET.SubElement(resource, 'city value=\"{}\"'.format(city))
    ET.SubElement(resource, 'district value=\"{}\"'.format(district))
    ET.SubElement(resource, 'postalCode value=\"{}\"'.format(postalCode))
    ET.SubElement(resource, 'country value=\"{}\"'.format(country))


def coding_type(resource, system, code, display=None, userSelected="false", version="4.0.1"):
    ET.SubElement(resource, 'system value=\"{}\"'.format(system))
    ET.SubElement(resource, 'version value=\"{}\"'.format(version))
    ET.SubElement(resource, 'code value=\"{}\"'.format(code))
    if display:
        ET.SubElement(resource, 'display value=\"{}\"'.format(display))
    ET.SubElement(resource, 'userSelected value=\"{}\"'.format(userSelected))


def contactpoint_type(resource, system, value, use=None, rank=None, period=None):
    ET.SubElement(resource, 'system value=\"{}\"'.format(system))
    ET.SubElement(resource, 'value value=\"{}\"'.format(value))
    if not use:
        use = "mobile"
    ET.SubElement(resource, 'use value=\"{}\"'.format(use))
    if rank:
        ET.SubElement(resource, 'rank value=\"{}\"'.format(rank))
    if period:
        period_type(resource, period)

def codeable_concept(resource, num_code, codes, text=None):
    for i in range(num_code):
        coding = ET.SubElement(resource, 'coding')
        coding_type(coding, codes['codes'][i].get('system'), codes['codes'][i].get('code'), codes['codes'][i].get('display'))
    if text:
        ET.SubElement(resource, 'text value=\"{}\"'.format(text))

def quantity_type(resource, value, unit, system, code,comparator=None):
    ET.SubElement(resource, 'value value=\"{}\"'.format(value))
    if comparator:
        ET.SubElement(resource, 'comparator value=\"{}\"'.format(comparator))
    ET.SubElement(resource, 'unit value=\"{}\"'.format(unit))
    ET.SubElement(resource, 'system value=\"{}\"'.format(system))
    ET.SubElement(resource, 'code value=\"{}\"'.format(code))

def money_type(resource, value, currency):
    ET.SubElement(resource, 'value value=\"{}\"'.format(value))
    ET.SubElement(resource, 'currency value=\"{}\"'.format(currency))

def range_type(resource, low_limit, high_limit):
    low = ET.SubElement(resource, 'low')
    quantity_type(low, low_limit.value, low_limit.comparator, low_limit.unit, low_limit.system, low_limit.code)
    high = ET.SubElement(resource, 'high')
    quantity_type(high, high_limit.value, high_limit.comparator, high_limit.unit, high_limit.system, high_limit.code)

def ratio_type(resource, numerator_value, denominator_value):
    numerator = ET.SubElement(resource, 'numerator')
    quantity_type(numerator, numerator_value.value, numerator_value.comparator, numerator_value.unit, numerator_value.system, numerator_value.code)
    denominator = ET.SubElement(resource, 'denominator')
    quantity_type(denominator, denominator_value.value, denominator_value.comparator, denominator_value.unit, denominator_value.system, denominator_value.code)

def duration_type(resource, value, unit, system, code):
    ET.SubElement(resource, 'value value=\"{}\"'.format(value))
    ET.SubElement(resource, 'unit value=\"{}\"'.format(unit))
    ET.SubElement(resource, 'system value=\"{}\"'.format(system))
    ET.SubElement(resource, 'code value=\"{}\"'.format(code))