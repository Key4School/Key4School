//determines if the user has a set theme
function detectColorScheme(){
  if(window.matchMedia("(prefers-color-scheme: dark)").matches) {
    localStorage.setItem('theme', 'dark');
    document.documentElement.setAttribute('data-theme', 'dark');
  }
  else {
    localStorage.setItem('theme', 'light');
    document.documentElement.setAttribute('data-theme', 'light');
  }
}
detectColorScheme();
