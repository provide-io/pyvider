// Initialize Mermaid for diagram rendering
// Provide.io shared configuration
document$.subscribe(function() {
  mermaid.initialize({
    startOnLoad: true,
    theme: 'default',
    themeVariables: {
      primaryColor: '#6366f1',
      primaryTextColor: '#fff',
      primaryBorderColor: '#4f46e5',
      lineColor: '#6366f1',
      secondaryColor: '#818cf8',
      tertiaryColor: '#c7d2fe'
    }
  });
});
