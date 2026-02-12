# Instructions for setting up a local environment to run labs in place of GitHub Codespace


<br><br>

These instructions will guide you through configuring a local environment that you can use to do the labs. 

<br><br>


**1. Use Git to clone this repository down to your machine with a command like the following.**

```
git clone https://github.com/skilldevai/ae-security
```

<br><br>

**2. Open up the cloned project in VS Code.** 

There are multiple ways to do this: 
- You can drag and drop the project directory onto VS Code.
- You can open VS Code and open the folder from its menu.
- You can simply change into the cloned directory and run the command "code ."

```
cd ae-security
code .
```

<br><br>

**3. Once you open the folder/project in VS Code, VS Code should detect the devcontainer setup and prompt you about running it as a development container (usually in lower right corner). Do not choose this option. Instead just click on the "x" to close the dialog and ignore that option.** 

<br>

![Starting in VS Code](./images/local-5.png?raw=true "Starting in VS Code")

<br>

**If you get a popup about "Not all host requirements in devcontainer.json are met by the Docker daemon", you can just click *Continue* and it will probably still be fine.**

![Host requirements](./images/local-6.png?raw=true "Host requirements")

<br><br>


**8. Allow the setup processing to run automatically. (May take up to 10 minutes for some projects).**

<br>

![Setup](./images/local-7.png?raw=true "Setup")

<br><br>

**9. When the processing is done, you'll see a message like "Done. Press any key to close the terminal."**

<br>

![Done](./images/local-8.png?raw=true "Done")

<br><br>

**10. Once you hit a key, that terminal will go away. To get a new terminal, you can either drag up from the bottom or use the *Terminal* -> *New terminal* command from the VS Code menu.**

<br>

![Terminal](./images/local-9.png?raw=true "terminal")

<br><br>

**11. You are now ready to run the labs in your local environment!**

<br><br>

---

## License and Use

These materials are provided as part of the **Enterprise AI Accelerator Workshop** conducted by **TechUpSkills (Brent Laster)**.

Use of this repository is permitted **only for registered workshop participants** for their own personal learning and
practice. Redistribution, republication, or reuse of any part of these materials for teaching, commercial, or derivative
purposes is not allowed without written permission.

© 2025 TechUpSkills / Brent Laster. All rights reserved.
