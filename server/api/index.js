// TODO: add API router here and all API sub-routers

const express = require('express');
const apiRouter = express.Router();

const { requireUser } = require('../auth/utils');

const { PrismaClient } = require("@prisma/client");
const prisma = new PrismaClient();

async function main() {
    // ... you will write your Prisma Client queries here
}

// main()
//     .then(async () => {
//         await prisma.$disconnect()
//     })
//     .catch(async (e) => {
//         console.error(e)
//         await prisma.$disconnect()
//         process.exit(1)
//     })


apiRouter.get("/test", (req, res) => {
    res.send({ message: "API is working!" });
});


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
        const updatedFaceShape = await prisma.faceShape.update({
            where:
                { id: Number(req.params.id) },
            data:
                { name },
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
        const updatedFaceShape = await prisma.faceShape.update({
            where:
                { id: Number(req.params.id) },
            data:
                { name },
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
        const skinToneId = Number(req.params.id); // Ensure it's a number
        const SingleSkinTone = await prisma.skinTone.findUnique({
            where: { id: skinToneId },
        });
        console.log('Fetched SkinTone:', SingleSkinTone); // Log the fetched data
        if (!SingleSkinTone) {
            return res.status(404).send({ error: "SkinTone not found" });
        }
        res.json(SingleSkinTone);
    // res.send(SingleSkinTone);
    } catch (error) {
        next(error);
    }
});



// POST /api/skintone
apiRouter.post("/skintone", async (req, res, next) => {
    try {
        // Step 2: Extract data from the request body
        const { name } = req.body;
        
        // Step 3: Create a new SkinTone record in the database
        const newSkinTone = await prisma.skinTone.create({
            data: { name },
        });

        // Log the created record for debugging purposes
        console.log('Created new SkinTone:', newSkinTone);

        // Step 4: Send the created SkinTone record as JSON
        res.status(201).send(newSkinTone); // Ensure it's JSON

    } catch (error) {
        console.error('Error in POST /api/skintone:', error); // Log any errors
        next(error);
    }
});



// PUT /api/skintone/:id
apiRouter.put("/skintone/:id", async (req, res, next) => {
    try {
        const { name } = req.body;
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
        res.send(updatedSkinType);
    } catch (error) {
        next(error);
    }
});


// //<--------------------------------GET COMMENTS BY USER----------------------------->

// //GET /api/:user/comments 
// apiRouter.get("/:user/comments", requireUser, async (req, res, next) => {
//     try {
//         const comments = await prisma.comment.findMany({
//             where: { userId: req.user.id },
//             include: { user: true }
//         });
//         res.send(comments);
//     } catch (error) {
//         next(error);
//     }
// });



module.exports = apiRouter;