# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/PatrickBaus/tinkerforge_async/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                             |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|----------------------------------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| tinkerforge\_async/\_\_init\_\_.py                               |        5 |        0 |        0 |        0 |    100% |           |
| tinkerforge\_async/async\_event\_bus.py                          |       22 |       15 |        4 |        0 |     27% |18, 34-48, 61-63 |
| tinkerforge\_async/brick\_master/\_\_init\_\_.py                 |        8 |        0 |        0 |        0 |    100% |           |
| tinkerforge\_async/brick\_master/chibi.py                        |       80 |       46 |       18 |        0 |     35% |48-51, 61-64, 75-78, 89-92, 103-106, 126-131, 151-166, 173-180, 186-192, 199-202, 211-214, 232-235, 246-249, 269, 280-283 |
| tinkerforge\_async/brick\_master/common.py                       |      136 |        2 |        0 |        0 |     99% |   174-178 |
| tinkerforge\_async/brick\_master/ethernet.py                     |       86 |       43 |       26 |        0 |     38% |75-79, 117-139, 161-166, 182-186, 199-213, 232-239, 267-272, 291-295, 314-319, 333-337 |
| tinkerforge\_async/brick\_master/master.py                       |      173 |       74 |       24 |        0 |     50% |150-153, 161-164, 189-194, 205-211, 217-221, 234, 247-251, 265, 278-282, 295, 308-312, 340-343, 363-368, 400-403, 423-428, 460-463, 483-488, 565, 578-581, 594-603, 628-631, 644-653, 672-681, 694, 709, 719-722, 732-741, 751-755, 758-762 |
| tinkerforge\_async/brick\_master/rs485.py                        |       67 |       39 |       18 |        0 |     33% |47-50, 61-64, 75-78, 95-100, 116-131, 138-145, 151-156, 165-169, 188-193, 204-209 |
| tinkerforge\_async/brick\_master/wifi2.py                        |      319 |      174 |      100 |        0 |     35% |222-226, 243-252, 268-285, 301-310, 329-334, 348-352, 397-414, 430-437, 445-469, 531-565, 589-596, 614-626, 639-642, 656-661, 678-685, 736-768, 794-802, 827-832, 849-856, 869-872, 880-883, 890-893, 901, 911, 921-924, 974-1026, 1054-1069, 1100-1105, 1120-1123, 1140-1145, 1160-1167, 1177-1185, 1195-1199, 1215-1219 |
| tinkerforge\_async/brick\_master/wifi.py                         |      237 |      110 |       56 |        0 |     43% |154, 157-159, 166, 173, 177-179, 186, 190-192, 199, 203-205, 252-255, 296-325, 346-351, 407-421, 446-460, 486-492, 514, 523-530, 537-538, 545-552, 559-560, 585, 604-611, 626-629, 640-644, 659-663, 679-682, 693-697, 709-714, 730-734, 745-759, 774-778, 797-802, 816-820 |
| tinkerforge\_async/bricklet\_ambient\_light\_v2.py               |      110 |       33 |       14 |        0 |     62% |168-171, 180-183, 194-197, 221-228, 241-247, 263-268, 279-282, 314-319, 330-334, 337 |
| tinkerforge\_async/bricklet\_ambient\_light\_v3.py               |       95 |       27 |       12 |        0 |     64% |156-160, 198-207, 227-233, 264-269, 280-285, 288 |
| tinkerforge\_async/bricklet\_analog\_in.py                       |      129 |       47 |       16 |        0 |     57% |164-167, 181-184, 193-196, 207-210, 219-222, 233-236, 260-263, 276-282, 306-309, 320-325, 343-348, 359-362, 377-380, 393-396, 407-410, 423-426, 429-431 |
| tinkerforge\_async/bricklet\_barometer.py                        |      130 |       46 |       20 |        2 |     57% |149-152, 163-166, 177, 203-206, 217-220, 244-247, 265-271, 295-298, 316-322, 341, 356-359, 386-392, 403-406, 427-442, 462-465, 468-470 |
| tinkerforge\_async/bricklet\_barometer\_v2.py                    |      161 |       43 |       22 |        5 |     67% |180-183, 223, 225, 227, 267-270, 310, 332-338, 396, 440-451, 468-472, 485, 496-500, 521, 538-546, 564-569, 586-592, 595-599 |
| tinkerforge\_async/bricklet\_humidity.py                         |       97 |       36 |       12 |        0 |     56% |141-144, 164-167, 179-182, 193-196, 208-211, 222-225, 251-254, 267-273, 299-302, 313-317, 337-342, 353-356, 359-361 |
| tinkerforge\_async/bricklet\_humidity\_v2.py                     |      122 |       46 |       18 |        0 |     54% |158-161, 204-213, 233-239, 251-254, 298-302, 322-328, 339-342, 353-357, 385-396, 413-417, 431-434, 451-455, 458-460 |
| tinkerforge\_async/bricklet\_industrial\_dual\_0\_20ma\_v2.py    |      125 |       40 |       18 |        0 |     61% |186-195, 235-241, 262-272, 294-296, 307-311, 320-322, 333-335, 349-353, 364-374, 403-407, 426-437 |
| tinkerforge\_async/bricklet\_industrial\_dual\_analog\_in\_v2.py |      150 |       60 |       22 |        0 |     52% |189-198, 237-243, 264-273, 285-289, 306-309, 328-332, 339-341, 352-356, 367, 378-382, 389-393, 405-409, 427-437, 465-469, 488-501, 504-513 |
| tinkerforge\_async/bricklet\_industrial\_ptc.py                  |        5 |        0 |        0 |        0 |    100% |           |
| tinkerforge\_async/bricklet\_io4\_v2.py                          |      262 |      147 |       78 |        2 |     34% |196, 209-212, 225-228, 268-273, 291-302, 316-321, 326-339, 361-364, 383-393, 409, 427-431, 455-478, 481-483, 503, 528, 550-565, 592-597, 619-630, 649-652, 670-680, 683-702, 705-708, 733-760, 767-796 |
| tinkerforge\_async/bricklet\_io16.py                             |      200 |       77 |       60 |        4 |     52% |170-178, 190-199, 227-242, 263-272, 286-290, 295-298, 309-314, 325-328, 339-348, 359-368, 395-411, 422-434, 452-466, 482-491, 518, 538, 574, 583 |
| tinkerforge\_async/bricklet\_isolator.py                         |       67 |       18 |        2 |        0 |     71% |115-125, 161, 172-175, 195, 206-212, 227-233, 254-257, 277-281, 284 |
| tinkerforge\_async/bricklet\_moisture.py                         |       77 |       26 |       10 |        0 |     59% |122-125, 134-137, 148-151, 175-181, 199-203, 219-224, 235-238, 247-250, 261-264 |
| tinkerforge\_async/bricklet\_motion\_detector\_v2.py             |       53 |       16 |        8 |        0 |     61% |90-93, 106-109, 120-123, 133-140, 158-162 |
| tinkerforge\_async/bricklet\_ptc.py                              |      160 |       60 |       14 |        0 |     57% |151, 168, 204-207, 222-225, 237-240, 251-254, 264-267, 278-281, 307-309, 327-333, 359-361, 379-385, 403-408, 419-422, 435-437, 449-452, 462-465, 475-477, 488-491, 502, 515-518, 524-527, 530-532, 535-539 |
| tinkerforge\_async/bricklet\_ptc\_v2.py                          |      159 |       65 |       30 |        1 |     50% |140, 145, 159, 194-197, 236-241, 261-267, 282-285, 323-332, 352-358, 369-372, 383-386, 398-401, 410-413, 424-427, 450-461, 478-482, 495, 508-511, 517-520, 523-525, 528-532 |
| tinkerforge\_async/bricklet\_rs232\_v2.py                        |      190 |      100 |       44 |        0 |     38% |156-161, 172-187, 199-224, 232-237, 246-250, 264-271, 291-296, 318-334, 345-349, 357-361, 367-371, 385-388, 401-405, 417-442, 449-452, 465-493, 496-511 |
| tinkerforge\_async/bricklet\_segment\_display\_4x7.py            |       52 |       13 |       12 |        4 |     67% |98-106, 125-128, 152, 154, 156, 158, 184-187 |
| tinkerforge\_async/bricklet\_segment\_display\_4x7\_v2.py        |       75 |       33 |       16 |        0 |     46% |78-80, 101-111, 122-125, 133-136, 147-150, 169-171, 189-192, 203-213, 228-235, 256-259 |
| tinkerforge\_async/bricklet\_temperature.py                      |       81 |       23 |        4 |        0 |     68% |136-139, 151-154, 165-168, 194-196, 209-215, 233-238, 249-252, 270-272, 285-288 |
| tinkerforge\_async/bricklet\_temperature\_v2.py                  |       66 |       18 |        6 |        0 |     67% |122-125, 169-174, 194-200, 208-211, 222-226, 229 |
| tinkerforge\_async/bricklet\_thermocouple\_v2.py                 |      130 |       42 |       22 |        1 |     59% |138, 143, 158, 198-201, 242-247, 267-273, 307-315, 323-328, 344-349, 355-359, 362-366, 369-371 |
| tinkerforge\_async/device\_factory.py                            |       61 |        4 |        0 |        0 |     93% |     59-62 |
| tinkerforge\_async/devices.py                                    |      301 |       36 |       32 |        1 |     88% |237, 374, 381, 394-403, 466, 538, 545, 576, 644-652, 658-661, 672-675, 693-699, 712-714, 725-728, 737-740, 752-755, 771-775, 791 |
| tinkerforge\_async/helper.py                                     |       38 |       23 |       10 |        0 |     31% |     35-62 |
| tinkerforge\_async/ip\_connection.py                             |      328 |      230 |       68 |        0 |     25% |26-27, 125, 132, 139, 146, 154, 161, 170-196, 199, 206, 209-210, 215, 230-250, 256-262, 275-301, 317-318, 322-327, 334-335, 338-339, 385-441, 453-490, 495-516, 523-525, 531-544, 550-559, 565-571, 574-586, 599-614, 628-661, 670-686, 690-707 |
| tinkerforge\_async/ip\_connection\_helper.py                     |       85 |       38 |       48 |       10 |     55% |17-26, 30-37, 41-49, 58-67, 72, 76, 78, 88, 96, 108-109, 117, 122, 125 |
| tinkerforge\_async/quantities.py                                 |       15 |        0 |        0 |        0 |    100% |           |
| **TOTAL**                                                        | **4657** | **1850** |  **864** |   **30** | **52%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/PatrickBaus/tinkerforge_async/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/PatrickBaus/tinkerforge_async/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/PatrickBaus/tinkerforge_async/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/PatrickBaus/tinkerforge_async/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2FPatrickBaus%2Ftinkerforge_async%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/PatrickBaus/tinkerforge_async/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.