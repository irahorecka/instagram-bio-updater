// Node file to log into IG and update IG bio with content from bio.txt.

const dotenv = require('dotenv');
const fs = require('fs');
const path = require('path');
const { IgApiClient } = require("instagram-private-api");
const ig = new IgApiClient();
const BASEPATH = path.dirname(require.main.filename);

dotenv.config({ path: path.join(BASEPATH, '.env') });

const USERNAME = process.env.IG_USER;
const PASSWORD = process.env.IG_PASS;

ig.state.generateDevice(USERNAME);

// Read file as exported by Python.
try {
    var data = fs.readFileSync(path.join(BASEPATH, 'bio.txt'), 'utf8');
    console.log(data.toString());
} catch(e) {
    console.log('Error:', e.stack);
}

// Async func to log in and update IG bio
const main = async () => {
  await ig.simulate.preLoginFlow();
  await ig.account.login(USERNAME, PASSWORD);

  // Log out of Instagram when done.
  process.nextTick(async () => await ig.simulate.postLoginFlow());

  // Fill in whatever you want your new Instagram bio to be.
  await ig.account.setBiography(data.toString());
}

main();
