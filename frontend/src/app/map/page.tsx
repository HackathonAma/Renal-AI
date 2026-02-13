"use client";

import React from 'react';
import dynamic from 'next/dynamic';
import { Map as MapIcon } from 'lucide-react';
import Navbar from '@/components/Navbar';

// Dynamically import the map component to avoid SSR issues with Leaflet
const BeninMap = dynamic(() => import('@/components/Map/BeninMap'), {
    ssr: false,
    loading: () => (
        <div className="w-full h-full flex items-center justify-center">
            <div className="text-center space-y-4">
                <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto" />
                <p className="text-sm font-bold text-muted">Chargement de la carte...</p>
            </div>
        </div>
    ),
});

export default function MapPage() {
    return (
        <div className="h-screen flex flex-col bg-white overflow-hidden">
            <Navbar />

            <main className="flex-1 flex flex-col p-6 lg:p-10 gap-6 overflow-hidden">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        <div className="bg-primary/10 p-2.5 rounded-2xl">
                            <MapIcon className="text-primary w-6 h-6" />
                        </div>
                        <div>
                            <h1 className="text-2xl font-black font-outfit text-slate-900 tracking-tight leading-none">Cartographie Géo-Médicale</h1>
                            <p className="text-muted text-[10px] font-bold uppercase tracking-widest mt-1">Zones de prévalence de l'IRC au Bénin</p>
                        </div>
                    </div>

                    {/* Legend */}
                    <div className="hidden lg:flex items-center gap-6 text-[10px] font-bold uppercase tracking-widest">
                        <div className="flex items-center gap-2">
                            <div className="w-3 h-3 rounded-full bg-error" />
                            <span className="text-slate-600">Élevé (&gt;25%)</span>
                        </div>
                        <div className="flex items-center gap-2">
                            <div className="w-3 h-3 rounded-full bg-warning" />
                            <span className="text-slate-600">Modéré (15-25%)</span>
                        </div>
                        <div className="flex items-center gap-2">
                            <div className="w-3 h-3 rounded-full bg-success" />
                            <span className="text-slate-600">Faible (&lt;15%)</span>
                        </div>
                    </div>
                </div>

                <div className="flex-1 medical-card rounded-[2.5rem] overflow-hidden shadow-xl">
                    <BeninMap />
                </div>
            </main>
        </div>
    );
}
