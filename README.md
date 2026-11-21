# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/PatrickBaus/tinkerforge_async/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                             |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|----------------------------------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| tinkerforge\_async/\_\_init\_\_.py                               |        5 |        0 |        0 |        0 |    100% |           |
| tinkerforge\_async/async\_event\_bus.py                          |       22 |       15 |        4 |        0 |     27% |18, 34-48, 61-63 |
| tinkerforge\_async/brick\_master/\_\_init\_\_.py                 |        8 |        0 |        0 |        0 |    100% |           |
| tinkerforge\_async/brick\_master/chibi.py                        |       78 |       44 |       16 |        0 |     36% |48-51, 61-64, 75-78, 89-92, 103-106, 126-129, 149-164, 171-178, 184-190, 197-200, 209-212, 230-233, 244-247, 267, 278-281 |
| tinkerforge\_async/brick\_master/common.py                       |      136 |        2 |        0 |        0 |     99% |   174-178 |
| tinkerforge\_async/brick\_master/ethernet.py                     |       86 |       43 |       26 |        0 |     38% |75-79, 117-139, 161-166, 182-186, 199-213, 232-239, 267-272, 291-295, 314-319, 333-337 |
| tinkerforge\_async/brick\_master/master.py                       |      173 |       74 |       24 |        0 |     50% |150-153, 161-164, 189-194, 205-211, 217-221, 234, 247-251, 265, 278-282, 295, 308-312, 340-343, 363-368, 400-403, 423-428, 460-463, 483-488, 565, 578-581, 594-603, 628-631, 644-653, 672-681, 694, 709, 719-722, 732-741, 751-755, 758-762 |
| tinkerforge\_async/brick\_master/rs485.py                        |       65 |       37 |       16 |        0 |     35% |47-50, 61-64, 75-78, 95-98, 114-129, 136-143, 149-154, 163-167, 186-191, 202-207 |
| tinkerforge\_async/brick\_master/wifi2.py                        |      317 |      172 |       98 |        0 |     35% |177-181, 198-207, 223-240, 256-265, 284-289, 303-307, 352-369, 385-392, 400-424, 486-520, 544-551, 569-581, 594-597, 611-616, 633-640, 691-723, 749-757, 782-787, 804-811, 824-827, 835-838, 845-848, 856, 866, 876-879, 929-975, 1003-1018, 1049-1054, 1069-1072, 1089-1094, 1109-1116, 1126-1134, 1144-1148, 1164-1168 |
| tinkerforge\_async/brick\_master/wifi.py                         |      235 |      108 |       54 |        0 |     44% |129, 132-134, 141, 148, 152-154, 161, 165-167, 174, 178-180, 227-230, 271-300, 321-326, 382-391, 416-430, 456-462, 484, 493-500, 507-508, 515-522, 529-530, 555, 574-581, 596-599, 610-614, 629-633, 649-652, 663-667, 679-684, 700-704, 715-729, 744-748, 767-772, 786-790 |
| tinkerforge\_async/bricklet\_ambient\_light\_v2.py               |      110 |       33 |       14 |        0 |     62% |168-171, 180-183, 194-197, 221-228, 241-247, 263-268, 279-282, 314-319, 330-334, 337 |
| tinkerforge\_async/bricklet\_ambient\_light\_v3.py               |       94 |       26 |       12 |        0 |     64% |156-159, 197-206, 226-232, 263-268, 279-284, 287 |
| tinkerforge\_async/bricklet\_analog\_in.py                       |      129 |       47 |       16 |        0 |     57% |164-167, 181-184, 193-196, 207-210, 219-222, 233-236, 260-263, 276-282, 306-309, 320-325, 343-348, 359-362, 377-380, 393-396, 407-410, 423-426, 429-431 |
| tinkerforge\_async/bricklet\_barometer.py                        |      130 |       46 |       20 |        2 |     57% |149-152, 163-166, 177, 203-206, 217-220, 244-247, 265-271, 295-298, 316-322, 341, 356-359, 386-392, 403-406, 427-442, 462-465, 468-470 |
| tinkerforge\_async/bricklet\_barometer\_v2.py                    |      161 |       43 |       22 |        5 |     67% |180-183, 223, 225, 227, 267-270, 310, 332-338, 396, 440-451, 468-472, 485, 496-500, 521, 538-546, 564-569, 586-592, 595-599 |
| tinkerforge\_async/bricklet\_humidity.py                         |       97 |       36 |       12 |        0 |     56% |141-144, 164-167, 179-182, 193-196, 208-211, 222-225, 251-254, 267-273, 299-302, 313-317, 337-342, 353-356, 359-361 |
| tinkerforge\_async/bricklet\_humidity\_v2.py                     |      122 |       46 |       18 |        0 |     54% |158-161, 204-213, 233-239, 251-254, 298-302, 322-328, 339-342, 353-357, 385-396, 413-417, 431-434, 451-455, 458-460 |
| tinkerforge\_async/bricklet\_industrial\_dual\_0\_20ma\_v2.py    |      125 |       40 |       18 |        0 |     61% |186-195, 235-241, 262-272, 294-296, 307-311, 320-322, 333-335, 349-353, 364-374, 403-407, 426-437 |
| tinkerforge\_async/bricklet\_industrial\_dual\_analog\_in\_v2.py |      148 |       58 |       20 |        0 |     54% |189-198, 237-243, 264-273, 285-289, 306-309, 328-332, 339-341, 352-356, 367, 378-382, 389-393, 405-409, 427-437, 465-469, 488-501, 504-512 |
| tinkerforge\_async/bricklet\_industrial\_ptc.py                  |        5 |        0 |        0 |        0 |    100% |           |
| tinkerforge\_async/bricklet\_io4\_v2.py                          |      260 |      145 |       76 |        2 |     35% |199, 212-215, 228-231, 271-276, 294-305, 319-324, 329-338, 362-365, 384-394, 410, 428-432, 456-479, 482-484, 504, 529, 551-566, 593-598, 620-631, 650-653, 671-681, 684-703, 706-709, 734-761, 768-797 |
| tinkerforge\_async/bricklet\_io16.py                             |      200 |       77 |       60 |        4 |     52% |170-178, 190-199, 227-242, 263-272, 286-290, 295-298, 309-314, 325-328, 339-348, 359-368, 395-411, 422-434, 452-466, 482-491, 518, 538, 574, 583 |
| tinkerforge\_async/bricklet\_isolator.py                         |       68 |       19 |        2 |        0 |     70% |115-125, 161, 172-175, 195, 206-212, 227-233, 254-257, 277-281, 284-285 |
| tinkerforge\_async/bricklet\_moisture.py                         |       77 |       26 |       10 |        0 |     59% |122-125, 134-137, 148-151, 175-181, 199-203, 219-224, 235-238, 247-250, 261-264 |
| tinkerforge\_async/bricklet\_motion\_detector\_v2.py             |       55 |       17 |        8 |        0 |     60% |91-94, 107-110, 121-124, 134-141, 159-163, 167 |
| tinkerforge\_async/bricklet\_ptc.py                              |      160 |       60 |       14 |        0 |     57% |151, 168, 204-207, 222-225, 237-240, 251-254, 264-267, 278-281, 307-309, 327-333, 359-361, 379-385, 403-408, 419-422, 435-437, 449-452, 462-465, 475-477, 488-491, 502, 515-518, 524-527, 530-532, 535-539 |
| tinkerforge\_async/bricklet\_ptc\_v2.py                          |      159 |       65 |       30 |        1 |     50% |140, 145, 159, 194-197, 236-241, 261-267, 282-285, 323-332, 352-358, 369-372, 383-386, 398-401, 410-413, 424-427, 450-461, 478-482, 495, 508-511, 517-520, 523-525, 528-532 |
| tinkerforge\_async/bricklet\_rs232\_v2.py                        |      185 |       95 |       42 |        0 |     40% |156-161, 172-187, 199-222, 230-235, 244-248, 262-269, 289-294, 316-332, 343-347, 355-359, 365-369, 383-386, 399-403, 415-434, 441-444, 457-485, 488-503 |
| tinkerforge\_async/bricklet\_segment\_display\_4x7.py            |       52 |       13 |       12 |        4 |     67% |98-106, 125-128, 152, 154, 156, 158, 184-187 |
| tinkerforge\_async/bricklet\_segment\_display\_4x7\_v2.py        |       75 |       33 |       16 |        0 |     46% |78-80, 101-111, 122-125, 133-136, 147-150, 169-171, 189-192, 203-213, 228-235, 256-259 |
| tinkerforge\_async/bricklet\_temperature.py                      |       81 |       23 |        4 |        0 |     68% |136-139, 151-154, 165-168, 194-196, 209-215, 233-238, 249-252, 270-272, 285-288 |
| tinkerforge\_async/bricklet\_temperature\_v2.py                  |       66 |       18 |        6 |        0 |     67% |122-125, 169-174, 194-200, 208-211, 222-226, 229 |
| tinkerforge\_async/bricklet\_thermocouple\_v2.py                 |      130 |       42 |       22 |        1 |     59% |138, 143, 158, 198-201, 242-247, 267-273, 307-315, 323-328, 344-349, 355-359, 362-366, 369-371 |
| tinkerforge\_async/device\_factory.py                            |       61 |        4 |        0 |        0 |     93% |     59-62 |
| tinkerforge\_async/devices.py                                    |      301 |       36 |       32 |        1 |     88% |237, 374, 381, 394-403, 466, 538, 545, 576, 644-652, 658-661, 672-675, 693-699, 712-714, 725-728, 737-740, 752-755, 771-775, 791 |
| tinkerforge\_async/helper.py                                     |       38 |       23 |       10 |        0 |     31% |     35-62 |
| tinkerforge\_async/ip\_connection.py                             |      321 |      225 |       68 |        0 |     26% |119, 126, 133, 140, 148, 155, 164-190, 193, 200, 203-204, 209, 224-244, 250-256, 269-295, 312-313, 318-323, 330-331, 334-335, 381-437, 449-486, 491-512, 519-521, 527-536, 542-551, 557-563, 566-578, 591-606, 620-653, 662-678, 682-699 |
| tinkerforge\_async/ip\_connection\_helper.py                     |       85 |       38 |       48 |       10 |     55% |17-26, 30-37, 41-49, 58-67, 72, 76, 78, 88, 96, 108-109, 117, 122, 125 |
| tinkerforge\_async/quantities.py                                 |       15 |        0 |        0 |        0 |    100% |           |
| **TOTAL**                                                        | **4635** | **1829** |  **850** |   **30** | **53%** |           |


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