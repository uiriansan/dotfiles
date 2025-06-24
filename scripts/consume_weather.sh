#!/bin/bash

# Consume weather information from https://open-meteo.com and save to file every hour using cronie

# Refer to https://open-meteo.com/en/docs
API_URL="https://api.open-meteo.com/v1/forecast?latitude=-26.9978&longitude=-51.5561&current=temperature_2m,is_day,weather_code&timezone=America%2FSao_Paulo&forecast_days=1"
SAVE_FILE="$HOME/.config/scripts/weather.json"

API_DATA=$(curl -s "$API_URL")

IS_DAY=$(echo "$API_DATA" | jq -r ".current.is_day")
TEMPERATURE=$(echo "$API_DATA" | jq -r ".current.temperature_2m")
WEATHER_CODE=$(echo "$API_DATA" | jq -r ".current.weather_code")

ICON=""
COLOR=""

if (( $WEATHER_CODE >= 3 && $WEATHER_CODE <= 48 )); then
	# CLOUDY
	ICON="󰅟"
	COLOR="grey"
elif (( $WEATHER_CODE >= 49 && $WEATHER_CODE <= 86 )); then
	# RAIN
	ICON="󰖌"
	COLOR="blue"
elif (( $WEATHER_CODE >= 87 && $WEATHER_CODE <= 99 )); then
	# THUNDERSTORM
	ICON=""
	COLOR="#df1b1b"
else
	#CLEAR
	if (( $IS_DAY )); then
		ICON="󰖨"
		COLOR="yellow"
	else
		ICON=""
		COLOR="#343436"
	fi
fi

echo "{\"icon\": \"$ICON\",\"temp\":\"$TEMPERATURE\",\"color\": \"$COLOR\"}" > $SAVE_FILE

DT=$(date "+%d/%m/%Y %H:%M:%S");
echo "$DT: Success | DAY: $IS_DAY / TEMP: $TEMPERATURE / WMO: $WEATHER_CODE"
