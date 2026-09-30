@echo off
echo ============================================================
echo  Pushing TripGenie App to GitHub for Cherry-beep2007
echo ============================================================

git init
git add .
git commit -m "Deploying TripGenie AI Trip Planner"
git branch -M main
git remote add origin https://github.com/Cherry-beep2007/tripgenie.git
git push -u origin main

echo.
echo ============================================================
echo  Done! Now go to https://share.streamlit.io to deploy.
echo ============================================================
pause
