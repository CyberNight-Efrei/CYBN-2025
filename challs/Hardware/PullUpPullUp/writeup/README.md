Le pin RESET* (pour RESET à LOW) est tiré au GND par une résistance de pull-down. En le reliant à VCC, le pin est monté à HIGH grâce à la résistance, et le microcontrolleur peut donc démarrer normalement.

On lit ensuite le flag en série à 9600 bauds sur le pin 0 du microcontrolleur.
