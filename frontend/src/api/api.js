// src/api/api.js

/**
 * Base API URL - reads from environment variable or defaults to localhost
 */
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

/**
 * Generic API call function with error handling
 * @param {string} endpoint - API endpoint path
 * @param {object} data - Request body data
 * @returns {Promise<object>} - API response
 */
const apiCall = async (endpoint, data) => {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.error(`API call failed for ${endpoint}:`, error);
    throw error;
  }
};

/**
 * Run a specific ocean analysis model
 * @param {string} modelType - Type of model (pollution, coral, forecast, activity, anomalies, mehi)
 * @param {object} inputs - Input parameters for the model
 * @returns {Promise<object>} - Model results
 */
export const runModel = async (modelType, inputs) => {
  const validModels = ['pollution', 'coral', 'forecast', 'activity', 'anomalies', 'mehi'];
  
  if (!validModels.includes(modelType)) {
    throw new Error(`Invalid model type: ${modelType}. Must be one of: ${validModels.join(', ')}`);
  }

  return await apiCall(`/api/${modelType}/run`, inputs);
};

/**
 * Run pollution detection model
 * @param {object} params - { lat, lon, depth, salinity, temperature, pH }
 */
export const runPollutionModel = async (params) => {
  return await apiCall('/api/pollution/run', params);
};

/**
 * Run coral health analysis model
 * @param {object} params - { lat, lon, depth, temperature, pH, imageUrl? }
 */
export const runCoralModel = async (params) => {
  return await apiCall('/api/coral/run', params);
};

/**
 * Run ocean forecast model
 * @param {object} params - { lat, lon, depth, temperature, salinity }
 */
export const runForecastModel = async (params) => {
  return await apiCall('/api/forecast/run', params);
};

/**
 * Run human activity analysis model
 * @param {object} params - { lat, lon }
 */
export const runActivityModel = async (params) => {
  return await apiCall('/api/activity/run', params);
};

/**
 * Run anomaly detection model
 * @param {object} params - { lat, lon, depth, temperature, salinity, pH }
 */
export const runAnomaliesModel = async (params) => {
  return await apiCall('/api/anomalies/run', params);
};

/**
 * Run Marine Ecosystem Health Index (MEHI) model
 * @param {object} params - All available parameters
 */
export const runMehiModel = async (params) => {
  return await apiCall('/api/mehi/run', params);
};

/**
 * Run all models sequentially
 * @param {object} inputs - Complete input parameters
 * @param {function} onProgress - Callback for progress updates (modelName, result)
 * @returns {Promise<object>} - Object containing all model results
 */
export const runAllModels = async (inputs, onProgress = null) => {
  const models = ['pollution', 'coral', 'forecast', 'activity', 'anomalies', 'mehi'];
  const results = {};

  for (const model of models) {
    try {
      const result = await runModel(model, inputs);
      results[model] = result;
      
      if (onProgress) {
        onProgress(model, result);
      }
    } catch (error) {
      console.error(`Error running ${model} model:`, error);
      results[model] = { status: 'error', message: error.message };
    }
  }

  return results;
};

/**
 * Health check endpoint to verify API connection
 * @returns {Promise<object>} - Server health status
 */
export const healthCheck = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/health`, {
      method: 'GET',
    });

    if (!response.ok) {
      throw new Error(`Health check failed with status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Health check failed:', error);
    throw error;
  }
};

/**
 * Test API connection with timeout
 * @param {number} timeout - Timeout in milliseconds (default: 5000)
 * @returns {Promise<boolean>} - True if connection successful
 */
export const testConnection = async (timeout = 5000) => {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(`${API_BASE_URL}/api/health`, {
      method: 'GET',
      signal: controller.signal,
    });
    clearTimeout(timeoutId);
    return response.ok;
  } catch (error) {
    clearTimeout(timeoutId);
    console.error('Connection test failed:', error);
    return false;
  }
};

/**
 * Validate input parameters before sending to API
 * @param {object} inputs - Input parameters to validate
 * @returns {object} - { valid: boolean, errors: string[] }
 */
export const validateInputs = (inputs) => {
  const errors = [];
  
  // Required fields
  const required = ['lat', 'lon', 'depth', 'salinity', 'temperature', 'pH'];
  
  for (const field of required) {
    if (!inputs[field] && inputs[field] !== 0) {
      errors.push(`${field} is required`);
    }
  }

  // Validate ranges
  if (inputs.lat && (inputs.lat < -90 || inputs.lat > 90)) {
    errors.push('Latitude must be between -90 and 90');
  }

  if (inputs.lon && (inputs.lon < -180 || inputs.lon > 180)) {
    errors.push('Longitude must be between -180 and 180');
  }

  if (inputs.depth && inputs.depth < 0) {
    errors.push('Depth must be positive');
  }

  if (inputs.salinity && (inputs.salinity < 0 || inputs.salinity > 50)) {
    errors.push('Salinity must be between 0 and 50 PSU');
  }

  if (inputs.temperature && (inputs.temperature < -2 || inputs.temperature > 40)) {
    errors.push('Temperature must be between -2 and 40°C');
  }

  if (inputs.pH && (inputs.pH < 6 || inputs.pH > 9)) {
    errors.push('pH must be between 6 and 9');
  }

  return {
    valid: errors.length === 0,
    errors
  };
};

/**
 * Format error message for user display
 * @param {Error} error - Error object
 * @returns {string} - Formatted error message
 */
export const formatErrorMessage = (error) => {
  if (error.message.includes('Failed to fetch')) {
    return 'Unable to connect to the server. Please ensure the backend is running.';
  }
  
  if (error.message.includes('Network request failed')) {
    return 'Network error. Please check your internet connection.';
  }
  
  return error.message || 'An unexpected error occurred. Please try again.';
};

// Export API base URL for direct access if needed
export { API_BASE_URL };

// Default export with all functions
export default {
  runModel,
  runPollutionModel,
  runCoralModel,
  runForecastModel,
  runActivityModel,
  runAnomaliesModel,
  runMehiModel,
  runAllModels,
  healthCheck,
  testConnection,
  validateInputs,
  formatErrorMessage,
  API_BASE_URL,
};