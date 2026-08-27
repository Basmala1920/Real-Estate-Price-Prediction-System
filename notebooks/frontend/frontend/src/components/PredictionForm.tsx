import React, { useState } from 'react';
import type { PredictionFormData } from '../types/prediction';
import locations from '../locations.json';

export const PredictionForm = () => {
  const [formData, setFormData] = useState<PredictionFormData>({
    location: locations[0] || 'other',
    carpet_area_sqft: 1000,
    floor_num: 1,
    bathroom: 2,
    balcony: 1,
    furnishing: 'Semi-Furnished',
    transaction: 'Resale',
    ownership: 'Freehold',
    facing: 'East'
  });

  const [price, setPrice] = useState<number | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
      const response = await fetch(`${baseUrl}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      if (!response.ok) throw new Error('فشل الاتصال بالخادم');
      
      const data = await response.json();
      setPrice(data.predicted_price);
    } catch (err) {
      setError('حدث خطأ أثناء التنبؤ بالسعر');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '40px auto', fontFamily: 'sans-serif', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
      <h2>House Price Prediction</h2>
      <form onSubmit={handleSubmit}>
        <label>Location:</label><br/>
        <select style={{ width: '100%', padding: '8px', marginBottom: '10px' }} value={formData.location} onChange={e => setFormData({...formData, location: e.target.value})}>
          {locations.map((loc: string) => <option key={loc} value={loc}>{loc}</option>)}
        </select>

        <label>Carpet Area (sqft):</label><br/>
        <input style={{ width: '95%', padding: '8px', marginBottom: '10px' }} type="number" min="1" value={formData.carpet_area_sqft} onChange={e => setFormData({...formData, carpet_area_sqft: +e.target.value})} required />

        <label>Floor Number:</label><br/>
        <input style={{ width: '95%', padding: '8px', marginBottom: '10px' }} type="number" value={formData.floor_num} onChange={e => setFormData({...formData, floor_num: +e.target.value})} required />

        <label>Bathrooms:</label><br/>
        <input style={{ width: '95%', padding: '8px', marginBottom: '10px' }} type="number" value={formData.bathroom} onChange={e => setFormData({...formData, bathroom: +e.target.value})} required />

        <button style={{ width: '100%', padding: '10px', background: '#007bff', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }} type="submit" disabled={loading}>
          {loading ? 'Predicting...' : 'Predict Price'}
        </button>
      </form>

      {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}
      {price !== null && (
        <div style={{ marginTop: '20px', padding: '10px', background: '#e0f7fa', borderRadius: '4px' }}>
          <h3>Predicted Price: ₹{(price / 100000).toFixed(2)} Lac</h3>
        </div>
      )}
    </div>
  );
};