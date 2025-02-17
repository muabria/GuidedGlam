// TODO: add API router here and all API sub-routers

const express = require('express');
const apiRouter = express.Router();

const { requireUser } = require('../auth/utils');

const { PrismaClient } = require("@prisma/client");
const prisma = new PrismaClient();

async function main() {
    // ... you will write your Prisma Client queries here
}

main()
    .then(async () => {
        await prisma.$disconnect()
    })
    .catch(async (e) => {
        console.error(e)
        await prisma.$disconnect()
        process.exit(1)
    })

apiRouter.get("/test", (req, res) => {
    res.send({ message: "API is working!" });
});

//<--------------------------------GET ALL FACESHAPES-------------------------------->

//GET /api/faceshape
apiRouter.get("/faceshape", async (req, res, next) => {
    try {
        const faceShapes = await prisma.faceShape.findMany();
        res.send(faceShapes);
    } catch (error) {
        next(error);
    }
});

//<--------------------------------GET SINGLE FACE SHAPE-------------------------------->

//GET /api/faceshape/:id
apiRouter.get("/faceshape/:id", async (req, res, next) => {
    try {
        const faceShape = await prisma.faceShape.findUnique({
            where: {
                id: Number(req.params.id)
            },
        });

        if (!faceShape) {
            return res.status(404).send({ error: "FaceShape not found" });
        }

        res.send(faceShape);
    } catch (error) {
        next(error);
    }
});

// POST /api/faceshape
apiRouter.post("/faceshape", async (req, res, next) => {
    try {
        const { name } = req.body;
        const newFaceShape = await prisma.faceShape.create({
            data: { name }
        });

        res.status(201).send(newFaceShape);
    } catch (error) {
        next(error);
    }
});

// PUT /api/faceshape/:id
apiRouter.put("/faceshape/:id", async (req, res, next) => {
    try {
        const { name } = req.body;
        const faceShape = await prisma.faceShape.findUnique({
            where: { id: Number(req.params.id) },
        });

        if (!faceShape) {
            return res.status(404).send({ error: "FaceShape not found" });
        }

        const updatedFaceShape = await prisma.faceShape.update({
            where: { id: Number(req.params.id) },
            data: { name },
        });

        res.send(updatedFaceShape);
    } catch (error) {
        next(error);
    }
});

// PATCH /api/faceshape/:id
apiRouter.patch("/faceshape/:id", async (req, res, next) => {
    try {
        const { name } = req.body;
        const faceShape = await prisma.faceShape.findUnique({
            where: { id: Number(req.params.id) },
        });

        if (!faceShape) {
            return res.status(404).send({ error: "FaceShape not found" });
        }

        const updatedFaceShape = await prisma.faceShape.update({
            where: { id: Number(req.params.id) },
            data: { name },
        });

        res.send(updatedFaceShape);
    } catch (error) {
        next(error);
    }
});

// <------------------------ ALL SKIN TONES ------------------------>
//GET /api/skintone
apiRouter.get("/skintone", async (req, res, next) => {
    try {
        const skinTones = await prisma.skinTone.findMany();
        res.send(skinTones);
    } catch (error) {
        next(error);
    }
});

// <------------------------ SINGLE SKIN TONE ------------------------>
//GET /api/skintone/:id
apiRouter.get("/skintone/:id", async (req, res, next) => {
    try {
        const skinTone = await prisma.skinTone.findUnique({
            where: { id: Number(req.params.id) },
        });

        if (!skinTone) {
            return res.status(404).send({ error: "SkinTone not found" });
        }

        res.send(skinTone);
    } catch (error) {
        next(error);
    }
});

// POST /api/skintone
apiRouter.post("/skintone", async (req, res, next) => {
    try {
        const { name } = req.body;
        const newSkinTone = await prisma.skinTone.create({
            data: { name },
        });

        res.status(201).send(newSkinTone);
    } catch (error) {
        next(error);
    }
});

// PUT /api/skintone/:id
apiRouter.put("/skintone/:id", async (req, res, next) => {
    try {
        const { name } = req.body;
        const skinTone = await prisma.skinTone.findUnique({
            where: { id: Number(req.params.id) },
        });

        if (!skinTone) {
            return res.status(404).send({ error: "SkinTone not found" });
        }

        const updatedSkinTone = await prisma.skinTone.update({
            where: { id: Number(req.params.id) },
            data: { name },
        });

        res.send(updatedSkinTone);
    } catch (error) {
        next(error);
    }
});

// PATCH /api/skintone/:id
apiRouter.patch("/skintone/:id", async (req, res, next) => {
    try {
        const { name } = req.body;
        const skinTone = await prisma.skinTone.findUnique({
            where: { id: Number(req.params.id) },
        });

        if (!skinTone) {
            return res.status(404).send({ error: "FaceShape not found" });
        }

        const updatedSkinTone = await prisma.skinTone.update({
            where: { id: Number(req.params.id) },
            data: { name },
        });

        res.send(updatedSkinTone);
    } catch (error) {
        next(error);
    }
});

// <------------------------ ALL SKIN TYPES ------------------------>
//GET /api/skintype
apiRouter.get("/skintype", async (req, res, next) => {
    try {
        const skinTypes = await prisma.skinType.findMany();
        res.send(skinTypes);
    } catch (error) {
        next(error);
    }
});

// <------------------------ SINGLE SKIN TYPE ------------------------>
//GET /api/skintype/:id
apiRouter.get("/skintype/:id", async (req, res, next) => {
    try {
        const skinType = await prisma.skinType.findUnique({
            where: { id: Number(req.params.id) },
        });

        if (!skinType) {
            return res.status(404).send({ error: "SkinType not found" });
        }

        res.send(skinType);
    } catch (error) {
        next(error);
    }
});

// POST /api/skintype
apiRouter.post("/skintype", async (req, res, next) => {
    try {
        const { name } = req.body;
        const newSkinType = await prisma.skinType.create({
            data: { name },
        });

        res.status(201).send(newSkinType);
    } catch (error) {
        next(error);
    }
});

// PUT /api/skintype/:id
apiRouter.put("/skintype/:id", async (req, res, next) => {
    try {
        const { name } = req.body;
        const updatedSkinType = await prisma.skinType.update({
            where: { id: Number(req.params.id) },
            data: { name },
        });

        if (!updatedSkinType) {
            return res.status(404).send({ error: "SkinType not found" });
        }

        res.send(updatedSkinType);
    } catch (error) {
        next(error);
    }
});

// PATCH /api/skintype/:id
apiRouter.patch("/skintype/:id", async (req, res, next) => {
    try {
        const { name } = req.body;
        const updatedSkinType = await prisma.skinType.update({
            where: { id: Number(req.params.id) },
            data: { name },
        });

        if (!updatedSkinType) {
            return res.status(404).send({ error: "SkinType not found" });
        }

        res.send(updatedSkinType);
    } catch (error) {
        next(error);
    }
});

module.exports = apiRouter;