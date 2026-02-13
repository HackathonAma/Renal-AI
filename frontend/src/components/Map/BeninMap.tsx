"use client";

import React from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default marker icons in Leaflet with Next.js
const fixLeafletIcon = () => {
    // @ts-ignore
    delete L.Icon.Default.prototype._getIconUrl;
    L.Icon.Default.mergeOptions({
        iconRetinaUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png',
        iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
        shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
    });
};

const departmentsData = [
    { name: 'Littoral (Cotonou)', coords: [6.3667, 2.4333], prevalence: 28, riskFactor: 'Hypertension', cases: 142 },
    { name: 'Atlantique', coords: [6.6667, 2.3333], prevalence: 22, riskFactor: 'Diabète', cases: 98 },
    { name: 'Ouémé', coords: [6.5, 2.6], prevalence: 19, riskFactor: 'Obésité', cases: 76 },
    { name: 'Borgou', coords: [9.35, 2.6167], prevalence: 15, riskFactor: 'Infections', cases: 54 },
    { name: 'Zou', coords: [7.1833, 2.0667], prevalence: 12, riskFactor: 'Hypertension', cases: 41 },
    { name: 'Mono', coords: [6.6333, 1.7167], prevalence: 11, riskFactor: 'Diabète', cases: 38 },
    { name: 'Atakora', coords: [10.3, 1.3833], prevalence: 8, riskFactor: 'Malnutrition', cases: 22 },
    { name: 'Alibori', coords: [11.1333, 2.9333], prevalence: 7, riskFactor: 'Infections', cases: 19 },
    { name: 'Donga', coords: [9.7, 1.6667], prevalence: 9, riskFactor: 'Inconnu', cases: 25 },
    { name: 'Collines', coords: [8.1, 2.3], prevalence: 10, riskFactor: 'Hypertension', cases: 31 },
    { name: 'Couffo', coords: [7.0, 1.8], prevalence: 13, riskFactor: 'Diabète', cases: 44 },
    { name: 'Plateau', coords: [7.0, 2.6333], prevalence: 14, riskFactor: 'Sédentarité', cases: 47 },
];

function SetViewOnClick({ animateRef }: { animateRef: boolean }) {
    const map = useMap();
    return null;
}

export default function BeninMap() {
    React.useEffect(() => {
        fixLeafletIcon();
    }, []);

    const getColor = (prevalence: number) => {
        return prevalence > 25 ? '#ef4444' : // High - Error red
            prevalence > 15 ? '#f59e0b' : // Medium - Warning amber
                '#10b981'; // Low - Success emerald
    };

    return (
        <MapContainer
            center={[9.3077, 2.3158]}
            zoom={7}
            className="w-full h-full z-0"
            scrollWheelZoom={true}
        >
            <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
            />

            {departmentsData.map((dept) => (
                <CircleMarker
                    key={dept.name}
                    center={dept.coords as [number, number]}
                    radius={Math.sqrt(dept.cases) * 2}
                    fillColor={getColor(dept.prevalence)}
                    color="white"
                    weight={2}
                    opacity={1}
                    fillOpacity={0.7}
                >
                    <Popup className="medical-popup">
                        <div className="p-2 space-y-2">
                            <h4 className="font-black font-outfit text-slate-900 border-b border-slate-100 pb-1">{dept.name}</h4>
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Prévalence</p>
                                    <p className="text-lg font-black font-outfit text-primary">{dept.prevalence}%</p>
                                </div>
                                <div>
                                    <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Cas Détectés</p>
                                    <p className="text-lg font-black font-outfit text-slate-900">{dept.cases}</p>
                                </div>
                            </div>
                            <div className="bg-slate-50 p-2 rounded-lg border border-slate-100">
                                <p className="text-[9px] font-bold text-slate-500 uppercase tracking-widest leading-none">Risque Majeur</p>
                                <p className="text-xs font-black text-error italic">{dept.riskFactor}</p>
                            </div>
                        </div>
                    </Popup>
                </CircleMarker>
            ))}
        </MapContainer>
    );
}
