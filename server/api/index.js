// TODO: add API router here and all API sub-routers

const express = require('express');
const apiRouter = express.Router();

// const { requireUser, requireAdmin } = require('../auth/utils');

const { PrismaClient } = require("@prisma/client");
const prisma = new PrismaClient();


// <------------------------ HOMEPAGE ------------------------>

// <------------------------ FACE SHAPE ------------------------>

// <------------------------ SKIN TONES ------------------------>

module.exports = apiRouter;