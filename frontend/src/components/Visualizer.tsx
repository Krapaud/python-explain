'use client'

import { ExecutionState } from '@/types/execution'
import { Pause, Play, SkipBack, SkipForward, Square } from 'lucide-react'
import { useEffect, useState } from 'react'

interface VisualizerProps {
    executionState: ExecutionState | null
    isExecuting: boolean
}

export default function Visualizer({ executionState, isExecuting }: VisualizerProps) {
    const [currentStep, setCurrentStep] = useState(0)
    const [isPlaying, setIsPlaying] = useState(false)

    useEffect(() => {
        if (executionState) {
            setCurrentStep(0)
            setIsPlaying(false)
        }
    }, [executionState])

    useEffect(() => {
        let interval: NodeJS.Timeout
        if (isPlaying && executionState && currentStep < executionState.total_steps - 1) {
            interval = setInterval(() => {
                setCurrentStep(prev => {
                    if (prev >= executionState.total_steps - 1) {
                        setIsPlaying(false)
                        return prev
                    }
                    return prev + 1
                })
            }, 1000)
        }
        return () => clearInterval(interval)
    }, [isPlaying, executionState, currentStep])

    const handlePlay = () => {
        if (executionState && currentStep < executionState.total_steps - 1) {
            setIsPlaying(!isPlaying)
        }
    }

    const handleNext = () => {
        if (executionState && currentStep < executionState.total_steps - 1) {
            setCurrentStep(prev => prev + 1)
            setIsPlaying(false)
        }
    }

    const handlePrevious = () => {
        if (currentStep > 0) {
            setCurrentStep(prev => prev - 1)
            setIsPlaying(false)
        }
    }

    const handleReset = () => {
        setCurrentStep(0)
        setIsPlaying(false)
    }

    if (isExecuting) {
        return (
            <div className="flex items-center justify-center h-full">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
                    <p className="text-gray-600">Exécution du code en cours...</p>
                </div>
            </div>
        )
    }

    if (!executionState) {
        return (
            <div className="flex items-center justify-center h-full">
                <div className="text-center text-gray-500">
                    <p className="text-lg mb-2">Prêt à visualiser</p>
                    <p className="text-sm">Cliquez sur "Exécuter" pour commencer</p>
                </div>
            </div>
        )
    }

    const currentStepData = executionState.steps[currentStep]

    return (
        <div className="h-full flex flex-col">
            {/* Contrôles de navigation */}
            <div className="bg-white border-b border-gray-300 p-4">
                <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-2">
                        <button
                            onClick={handlePrevious}
                            disabled={currentStep === 0}
                            className="btn-secondary p-2"
                        >
                            <SkipBack className="w-4 h-4" />
                        </button>

                        <button
                            onClick={handlePlay}
                            disabled={currentStep >= executionState.total_steps - 1}
                            className="btn-primary p-2"
                        >
                            {isPlaying ? (
                                <Pause className="w-4 h-4" />
                            ) : (
                                <Play className="w-4 h-4" />
                            )}
                        </button>

                        <button
                            onClick={handleNext}
                            disabled={currentStep >= executionState.total_steps - 1}
                            className="btn-secondary p-2"
                        >
                            <SkipForward className="w-4 h-4" />
                        </button>

                        <button
                            onClick={handleReset}
                            className="btn-secondary p-2"
                        >
                            <Square className="w-4 h-4" />
                        </button>
                    </div>

                    <div className="text-sm text-gray-600">
                        Étape {currentStep + 1} sur {executionState.total_steps}
                    </div>
                </div>

                {/* Barre de progression */}
                <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                        className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                        style={{
                            width: `${((currentStep + 1) / executionState.total_steps) * 100}%`
                        }}
                    ></div>
                </div>
            </div>

            {/* Contenu de la visualisation */}
            <div className="flex-1 p-4 overflow-auto">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                    {/* Variables locales */}
                    <div className="card p-4">
                        <h3 className="font-semibold mb-3 text-gray-800">Variables locales</h3>
                        <div className="space-y-2">
                            {currentStepData?.stack[0]?.locals.map((variable, index) => (
                                <div key={index} className="flex justify-between items-center p-2 bg-gray-50 rounded">
                                    <span className="font-mono text-sm text-gray-700">
                                        {variable.name}
                                    </span>
                                    <span className="font-mono text-sm text-primary-600">
                                        {JSON.stringify(variable.value)}
                                    </span>
                                </div>
                            )) || (
                                    <p className="text-gray-500 text-sm">Aucune variable locale</p>
                                )}
                        </div>
                    </div>

                    {/* Variables globales */}
                    <div className="card p-4">
                        <h3 className="font-semibold mb-3 text-gray-800">Variables globales</h3>
                        <div className="space-y-2">
                            {currentStepData?.stack[0]?.globals.map((variable, index) => (
                                <div key={index} className="flex justify-between items-center p-2 bg-gray-50 rounded">
                                    <span className="font-mono text-sm text-gray-700">
                                        {variable.name}
                                    </span>
                                    <span className="font-mono text-sm text-primary-600">
                                        {JSON.stringify(variable.value)}
                                    </span>
                                </div>
                            )) || (
                                    <p className="text-gray-500 text-sm">Aucune variable globale</p>
                                )}
                        </div>
                    </div>

                    {/* Pile d'appels */}
                    <div className="card p-4">
                        <h3 className="font-semibold mb-3 text-gray-800">Pile d'appels</h3>
                        <div className="space-y-2">
                            {currentStepData?.stack.map((frame, index) => (
                                <div key={index} className="p-3 bg-gray-50 rounded border-l-4 border-primary-500">
                                    <div className="font-mono text-sm font-semibold text-gray-800">
                                        {frame.function_name}
                                    </div>
                                    <div className="text-xs text-gray-600">
                                        Ligne {frame.line}
                                    </div>
                                </div>
                            )) || (
                                    <p className="text-gray-500 text-sm">Pile vide</p>
                                )}
                        </div>
                    </div>

                    {/* Sortie */}
                    <div className="card p-4">
                        <h3 className="font-semibold mb-3 text-gray-800">Sortie</h3>
                        <div className="bg-black text-green-400 font-mono text-sm p-3 rounded min-h-[100px] max-h-[200px] overflow-auto">
                            {currentStepData?.output.map((line, index) => (
                                <div key={index}>{line}</div>
                            )) || (
                                    <div className="text-gray-500">Aucune sortie</div>
                                )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
