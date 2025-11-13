import React, { createContext, useState, useContext } from 'react';

const OceanInputContext = createContext();

export const useOceanInput = () => {
  const context = useContext(OceanInputContext);
  if (!context) {
    throw new Error('useOceanInput must be used within OceanInputProvider');
  }
  return context;
};

export const OceanInputProvider = ({ children }) => {
  const [inputs, setInputs] = useState({
    lat: '',
    lon: '',
    depth: '',
    salinity: '',
    temperature: '',
    pH: '',
    imageUrl: ''
  });

  const updateInput = (field, value) => {
    setInputs(prev => ({ ...prev, [field]: value }));
  };

  const updateMultipleInputs = (updates) => {
    setInputs(prev => ({ ...prev, ...updates }));
  };

  return (
    <OceanInputContext.Provider value={{ inputs, updateInput, updateMultipleInputs }}>
      {children}
    </OceanInputContext.Provider>
  );
};