#!/usr/bin/bash

if grep -q 'center-focused-column "always"' ~/.config/niri/config.kdl; then
  sed -i 's/.*center-focused-column.*/  center-focused-column "never"/' ~/.config/niri/config.kdl
  niri msg action maximize-column
  sleep 0.5
  niri msg action maximize-column
else
  sed -i 's/.*center-focused-column.*/  center-focused-column "always"/' ~/.config/niri/config.kdl
  niri msg action center-column
fi
