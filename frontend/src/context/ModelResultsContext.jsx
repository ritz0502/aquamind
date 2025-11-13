import React, { createContext, useState, useContext, useEffect } from 'react';

const ModelResultsContext = createContext();

export const useModelResults = () => {
  const context = useContext(ModelResultsContext);
  if (!context) {
    throw new Error('useModelResults must be used within ModelResultsProvider');
  }
  return context;
};

export const ModelResultsProvider = ({ children }) => {
  const [results, setResults] = useState(() => {
    const saved = localStorage.getItem('aquamind_model_results');
    return saved ? JSON.parse(saved) : {
      pollution: null,
      coral: null,
      forecast: null,
      activity: null,
      anomalies: null,
      mehi: null
    };
  });

  useEffect(() => {
    localStorage.setItem('aquamind_model_results', JSON.stringify(results));
  }, [results]);

  const updateResult = (model, data) => {
    setResults(prev => ({ ...prev, [model]: data }));
  };

  const clearResults = () => {
    setResults({
      pollution: null,
      coral: null,
      forecast: null,
      activity: null,
      anomalies: null,
      mehi: null
    });
    localStorage.removeItem('aquamind_model_results');
  };

  return (
    <ModelResultsContext.Provider value={{ results, updateResult, clearResults }}>
      {children}
    </ModelResultsContext.Provider>
  );
};