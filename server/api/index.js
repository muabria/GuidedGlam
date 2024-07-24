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
//<--------------------------------FACE SHAPES-------------------------------->
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

// <------------------------ SKIN TONES ------------------------>


// <------------------------ SKIN TYPES ------------------------>

module.exports = apiRouter;