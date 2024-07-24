// TODO: add API router here and all API sub-routers

const express = require('express');
const apiRouter = express.Router();

// const { requireUser, requireAdmin } = require('../auth/utils');

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


//<--------------------------------GET ALL FACESHAPES-------------------------------->

//GET /api/FaceShape
apiRouter.get("/faceshape", async (req, res, next) => {
    try {
        const FaceShape = await prisma.faceShape.findMany();
        res.send(FaceShape);
    } catch (error) {
        next(error);
    }
});
//<-------------------------------- SINGLE FACE SHAPES-------------------------------->
//GET /api/FaceShape/:id
apiRouter.get("/faceshape/:id", async (req, res, next) => {
    try {
        const SingleFaceShape = await prisma.faceShape.findUnique({
            where: {
                id: Number(req.params.id)
            },
        });

        res.send(SingleFaceShape);
    } catch (error) {
        next(error);
    }
});

// <------------------------ ALL SKIN TONES ------------------------>
//GET /api/skintone
apiRouter.get("/skintone", async (req, res, next) => {
    try {
        const SkinTone = await prisma.skinTone.findMany();
        res.send(SkinTone);
    } catch (error) {
        next(error);
    }
});

// <------------------------ SINGLE SKIN TONES ------------------------>
//GET /api/skintone/:id
apiRouter.get("/skintone/:id", async (req, res, next) => {
    try {
        const SingleSkinTone = await prisma.skinTone.findUnique({
            where: {
                id: Number(req.params.id)
            },
        });

        res.send(SingleSkinTone);
    } catch (error) {
        next(error);
    }
});

// <------------------------ ALL SKIN TYPES ------------------------>
//GET /api/skintype
apiRouter.get("/skintype", async (req, res, next) => {
    try {
        const SkinType = await prisma.skinType.findMany();
        res.send(SkinType);
    } catch (error) {
        next(error);
    }
});

// <------------------------ SINGLE SKIN TYPES ------------------------>

//GET /api/skintype/:id
apiRouter.get("/skintype/:id", async (req, res, next) => {
    try {
        const SingleSkinType = await prisma.skinType.findUnique({
            where: {
                id: Number(req.params.id)
            },
        });

        res.send(SingleSkinType);
    } catch (error) {
        next(error);
    }
});

module.exports = apiRouter;