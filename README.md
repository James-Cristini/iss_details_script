## iss_details_script


A simple script to accept command line arguments and print details regarding the International Space Station.

This script uses the API: http://open-notify.org/

Accepts the following posiitonal command line argument: loc, pass, or people


### `loc`
The `loc` command prints the current location of the ISS as (LATITUDE, LONGITUDE)
* Example call:
    * `>>> python iss_details.py loc`
    * `The current location of the ISS, at time 2019/05/05 17:37:55, is (18.1555, 99.4591)`


### `pass`
the `pass` command also requires `-lat` and `-lon` arguments and prints a few upcoming passes for the ISS at the given pocation
* Example call:
    * `>>> python iss_details.py pass -lat 22.5 -lon 44.5`
    * ```There are 5 upcoming passes for location (22.5, 44.5):
        The ISS will be overhead location (22.5, 44.5) at time 2019/05/05 20:38:09 for 583 seconds
        The ISS will be overhead location (22.5, 44.5) at time 2019/05/05 22:14:31 for 590 seconds
        The ISS will be overhead location (22.5, 44.5) at time 2019/05/06 04:51:43 for 318 seconds
        The ISS will be overhead location (22.5, 44.5) at time 2019/05/06 06:26:11 for 638 seconds
        The ISS will be overhead location (22.5, 44.5) at time 2019/05/06 08:03:59 for 443 seconds```
* Note that not passing in a valid -lat AND -lon will raise a ValueError


### `people`
The `people` command prints the names of a craft (e.g. ISS) and the people aboard them
* Example call:
    * `>>> python iss_details.py people`
    * `There are 6 people aboard the ISS. They are: Oleg Kononenko, David Saint-Jacques, Anne McClain, Alexey Ovchinin, Nick Hague, Christina Koch`
