import visitorController from "@/controllers/visitorController.js";
import {defineStore} from "pinia";

export const useVisitorStore = defineStore('visitorStore', () => {
    const getVisitorById = async (id) => {
        return await visitorController.getVisitorById(id);
    };

    return { getVisitorById };
});