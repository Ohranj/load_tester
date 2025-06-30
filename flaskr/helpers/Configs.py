class Configs:
    actionsList = [
        {
            'id': 0,
            'human_type': 'Visit URL in Address Bar',
            'type': 'visit'
        },
        {
            'id': 1,
            'human_type': 'Click Element on Page',
            'type': 'click'
        },
        {
            'id': 2,
            'human_type': 'Action Field Input',
            'type': 'input'
        },
        {
            'id': 3,
            'human_type': 'Take Screenshot',
            'type': 'screenshot'
        },
        {
            'id': 4,
            'human_type': 'Sleep',
            'type': 'sleep'
        },
    ]
    elementLookups = [
        {
            'id': 0,
            'selector_type': 0,
            'human_type': 'Element Id',
        },
        {
            'id': 1,
            'selector_type': 1,
            'human_type': 'Element Class',
        },
        {
            'id': 2,
            'selector_type': 2,
            'human_type': 'Element Tag',
        },
        {
            'id': 3,
            'selector_type': 3,
            'human_type': 'Element Name',
        },
        {
            'id': 4,
            'selector_type': 4,
            'human_type': 'Element Link Text',
        },
        {
            'id': 5,
            'selector_type': 5,
            'human_type': 'Element CSS Selector',
        }
    ]
    fieldTypes = [
        {
            'id': 0,
            'human_type': 'Text Field',
            'type': 'text'
        },
        {
            'id': 1,
            'human_type': 'Numeric Field',
            'type': 'number'
        },
        {
            'id': 2,
            'human_type': 'Select Field',
            'type': 'select'
        },
        {
            'id': 3,
            'human_type': 'Checkbox',
            'type': 'checkbox'
        }
    ]