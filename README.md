# Turing Machine Simulator
## _A simple educational tool for visualizing a Turing Machine_

![Burning CPU](https://i.imgur.com/zPO4omF.jpg)

This desktop application allows the user to customize and build their own Turing Machine, by setting the number of states and the symbols it uses they're then able to test whatever word they want as a tape equivalent and visualize the outcome of each transition and character swap until the machine can't find another valid state.

For the purpuses of the educational simulation, we'll assume the tape is finite, there's only a single initial state, and multiple transitions using the same symbol on a single state aren't allowed.

The application features two possible input methods, manual and file:

![Application welcome screen](https://i.imgur.com/hFqz7Tx.png)

The manual method allows for more granular inputs, perfect for someone who's trying to play with a smaller machine:

![Application manual input screen](https://i.imgur.com/jOc6Xw2.png)

After inputting these base settings the application will then generate their very own transition table ready to be filled:

![Application transition table input screen](https://i.imgur.com/ZWQnEay.png)

Meanwhile the file method allows more flexibility and quicker iteration when testing:

![Application file input screen text field](https://i.imgur.com/AnogjRr.png)

![Application file input screen browser](https://i.imgur.com/sxmdWRT.png)

Ultimately the input method is up to the user, what really matters are the results!

![Application results screen](https://i.imgur.com/vYdqsZN.png)

They show a detailed log of every single transition, what was the previous value, how it was changed and it even shows how the tape ended up, perfect for learning how the machine ran step by step!


## Usage

- Run the application and choose the desired input method in the welcome screen

**Manual**
  * Insert and integer value for the number of states.
  * Insert and integer value for the main alphabet size.
  * Insert the main alphabet symbols.
  * Insert and integer value for the auxiliar alphabet size.
  * Insert the auxiliar alphabet symbols.
  * Insert the start symbol.
  * Insert the blank symbol.
  * Marvel at your very own custom transition table.
  * Insert each transition in this format:
    * [FUTURE_STATE][SWAP_LETTER][TAPE_POINTER_DIRECTION]
    * Where future state is an integer with the maximum value being N total states -1.
    * Swap letter has to be an existing symbol.
    * Tape pointer direction has to be either "L" or "l" for left or "R" or "r" for right.
    * Transitions can also be "x" or "X" if they're empty.
  * Set the initial state.
    * The machine has to have one and only one intial state.
  * Set the final states.
    * The machine has to have at least one final state.
  * Click the confirm button to lock in your transition table.
  * Insert a test word to see the results.

**File**
  * Either write, paste in or use the file browser to find a a .txt with a valid input.
  * Input formatting goes as follows:
    * [NUMBER_OF_STATES]
    * [MAIN_ALPHABET]
    * [AUXILIAR_ALPHABET]
    * [START_SYMBOL]
    * [BLANK_SYMBOL]
    * [INITIAL_STATE]
    * [TEST_WORD]
    * [TRANSITION_TABLE]
        * The table has the following format:
        * [IS_FINAL_STATE],[TRANSITION_0_0],[TRANSITION_0_N]
        * [IS_FINAL_STATE],[TRANSITION_N_0],[TRANSITION_N_N]
        * Where [IS_FINAL_STATE] is either T or F for true or false
        * Transitions assume a similar table structure to the manual input where columns will follow the input order: main alphabet symbols, then the auxiliar alphabet symbols, then the start symbol and finally the blank symbol.
        * An example transition could be "1AR" or "X" for an empty one.
        * Each transition is separated by a comma.
        * An example line could be "F,X,X,4AL,4BL,5<R,X" or "T,X,X,X,X,X,X".
        * Each line corresponds to a state and its transitions.
  * Here's a more practical example of a text input:

![Text input example](https://i.imgur.com/YSPlB3U.png)

## Packages used

This educational application was only made possible because of these amazing packages.

| Package | Link |
| ------ | ------ |
| PyQt6 | https://pypi.org/project/PyQt6/ |
| PyInstaller | https://pypi.org/project/pyinstaller/ |

## Building the application

If you want to build the application yourself from the source code:

**Windows**
1. Download Python from https://www.python.org/downloads/ and install it
2. Open a terminal and run this command to install the dependencies:
```sh
pip install PyQt6 PyInstaller
```
3. Navigate to the source code's directory and run this command to build the application:
```sh
pyInstaller main_window.py --onefile --noconsole --icon=logo.ico --add-data "resources;resources"
```
4. Run the newly created .exe in the "dist" folder

**Linux**
1. Download and install Python using the package manager from your distro:
* Ubuntu/Debian
```sh
sudo apt install python3
```
* Fedora
```sh
sudo dnf install python3
```
* CentOS/RHEL
```sh
sudo yum install centos-release-scl
sudo yum install rh-python36
scl enable rh-python36 bash
```
* Arch
```sh
sudo pacman -S python
```
2. Download and install the Package Installer for Python (pip):
```sh
python3 get-pip.py
```
3. Download and install the dependencies:
```sh
sudo pip3 install pyinstaller pyqt6
```
4. Navigate to the source code's directory and run this command to build the application:
```sh
python3 -m PyInstaller main_window.py --onefile --noconsole --icon=logo.ico --add-data "resources:resources"
```
5. Navigate to the newly created "dist" folder
6. Run this command on the main_window binary file to grant it permission to execute
```sh
chmod +x main_window
```
7. Run the application with this command:
```sh
./main_window
```

## Compatibility

This application currently runs on Windows 10 and Linux. I am looking into the possibility of adding a macOS release but I won't make any promises.

## Future development

This application does have a few possibilities for additional features which may include:

- Different Turing Machine variations
- Different automata implementations
- Saving manual inputs as .txt files that can be loaded later
- Threaded implementation to see the transitions running in real time