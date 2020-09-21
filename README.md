LYOI Power Controller
===

A simple script which reads power states via IPMI, and automatically shutdown when one power supply fails.

Works on Inspur NF5270M4 Server with dual power supplies, when one power is connected to UPS while the other is connected to AC power.

We use this because our UPS does not support serial communication. If you have any smart UPS, do not use this script and use your UPS management program instead.

Licensed under [WTFPL](LICENSE).

Code with ♥ by [Victor Huang](https://qwq.ren).