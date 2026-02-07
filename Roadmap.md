# CiteGuard Development Roadmap

## Phase 1: MVP (Weeks 1-6) - Core Functionality

### Week 1: Backend Foundation ✅ PARTIALLY COMPLETE

**Completed:**
- [x] Project structure setup
- [x] Core services implementation
  - [x] Similarity detection service
  - [x] Citation generation service
  - [x] Paraphrasing service
- [x] API routes scaffolding
- [x] Configuration management
- [x] Docker setup

**Remaining Tasks:**
- [ ] Database integration
  - [ ] Set up Alembic migrations
  - [ ] Implement database connection
  - [ ] Test CRUD operations
- [ ] User authentication
  - [ ] JWT token generation
  - [ ] Password hashing
  - [ ] Auth middleware
- [ ] Testing
  - [ ] Unit tests for services
  - [ ] API endpoint tests
  - [ ] Integration tests

**Deliverable**: Functional backend API with core analysis features

---

### Week 2: Extension Scaffold

**Tasks:**
- [ ] Extension project setup
  - [ ] Webpack configuration
  - [ ] TypeScript setup
  - [ ] Tailwind CSS configuration
- [ ] Background service worker
  - [ ] Message passing setup
  - [ ] API communication
  - [ ] Storage management
- [ ] Content script basics
  - [ ] Inject into Google Docs
  - [ ] Detect text selection
  - [ ] Extract document content
- [ ] Popup interface
  - [ ] Login/signup form
  - [ ] Settings panel
  - [ ] Quick stats display

**Deliverable**: Extension that can inject into Google Docs and communicate with backend

---

### Week 3: Real-time Analysis

**Tasks:**
- [ ] Content script enhancements
  - [ ] Text change detection
  - [ ] Debounced analysis trigger
  - [ ] Section-by-section analysis
- [ ] UI overlay
  - [ ] Highlight flagged text
  - [ ] Show similarity scores
  - [ ] Display recommendations
- [ ] Sidebar component
  - [ ] Analysis results panel
  - [ ] Source list
  - [ ] Citation suggestions
- [ ] Performance optimization
  - [ ] Caching strategy
  - [ ] Batch requests
  - [ ] Progressive loading

**Deliverable**: Real-time plagiarism detection working in Google Docs

---

### Week 4: Citation & Paraphrasing UI

**Tasks:**
- [ ] Citation interface
  - [ ] Source metadata input form
  - [ ] Style selector (APA, MLA, etc.)
  - [ ] One-click insertion
  - [ ] Source library management
- [ ] Paraphrasing interface
  - [ ] Select text to paraphrase
  - [ ] Show multiple alternatives
  - [ ] Explain changes
  - [ ] Accept/reject suggestions
- [ ] Keyboard shortcuts
  - [ ] Quick citation (Ctrl+Shift+C)
  - [ ] Paraphrase (Ctrl+Shift+P)
  - [ ] Analyze (Ctrl+Shift+A)

**Deliverable**: Complete citation and paraphrasing workflows

---

### Week 5: Integration & Testing

**Tasks:**
- [ ] End-to-end testing
  - [ ] User registration flow
  - [ ] Document analysis flow
  - [ ] Citation generation flow
  - [ ] Paraphrasing flow
- [ ] Bug fixes
  - [ ] Fix reported issues
  - [ ] Handle edge cases
  - [ ] Improve error messages
- [ ] Performance tuning
  - [ ] Optimize API response times
  - [ ] Reduce extension memory usage
  - [ ] Improve model loading
- [ ] Documentation
  - [ ] User guide
  - [ ] API documentation
  - [ ] Development docs

**Deliverable**: Stable, tested MVP ready for beta

---

### Week 6: Beta Launch

**Tasks:**
- [ ] Deployment
  - [ ] Backend to Railway/Render
  - [ ] Set up PostgreSQL
  - [ ] Configure Redis
  - [ ] SSL certificates
- [ ] Extension publishing
  - [ ] Create Chrome Web Store listing
  - [ ] Screenshots & demo video
  - [ ] Privacy policy
  - [ ] Publish as unlisted beta
- [ ] Beta testing
  - [ ] Recruit 20-30 ELTE students
  - [ ] Collect feedback
  - [ ] Track metrics
  - [ ] Iterate based on feedback

**Deliverable**: Live beta version with real users

---

## Phase 2: Enhanced Features (Weeks 7-12)

### Academic Database Integration
- [ ] Semantic Scholar API
- [ ] arXiv integration
- [ ] CrossRef DOI lookup
- [ ] Google Scholar scraping (careful!)

### Advanced Analysis
- [ ] Writing style detection
- [ ] Consistency checking
- [ ] Citation pattern analysis
- [ ] Document health dashboard

### Multi-platform Support
- [ ] Microsoft Word Online
- [ ] Notion support
- [ ] Overleaf integration
- [ ] Native app (Electron)

### Collaboration Features
- [ ] Team source libraries
- [ ] Shared document review
- [ ] Comments & suggestions
- [ ] Version history

---

## Phase 3: Growth & Scale (Weeks 13-24)

### Enterprise Features
- [ ] University licenses
- [ ] SSO integration
- [ ] Admin dashboard
- [ ] Usage analytics
- [ ] LMS integration (Canvas, Moodle)

### Advanced AI
- [ ] Fine-tuned paraphrasing model
- [ ] Custom citation styles
- [ ] Subject-specific analysis
- [ ] Multi-language support

### Mobile Apps
- [ ] iOS app (React Native)
- [ ] Android app (React Native)
- [ ] Mobile web optimization

---

## Technical Debt & Maintenance

### Ongoing Tasks
- [ ] Update dependencies monthly
- [ ] Security audits
- [ ] Performance monitoring
- [ ] User feedback review
- [ ] Bug triaging

### Infrastructure
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Automated testing
- [ ] Monitoring (Sentry, DataDog)
- [ ] Backup strategy
- [ ] Disaster recovery plan

---

## Metrics & Success Criteria

### MVP Success Metrics (End of Week 6)
- [ ] 100+ active users
- [ ] 4.0+ star rating
- [ ] <500ms average API response
- [ ] <5% error rate
- [ ] 80%+ user satisfaction

### Phase 2 Success Metrics (End of Week 12)
- [ ] 1,000+ active users
- [ ] 10+ university partnerships
- [ ] 50,000+ documents analyzed
- [ ] $2,000+ MRR (monthly recurring revenue)

### Phase 3 Success Metrics (End of Week 24)
- [ ] 10,000+ active users
- [ ] 100+ enterprise customers
- [ ] 1M+ documents analyzed
- [ ] $20,000+ MRR
- [ ] Featured on Product Hunt

---

## Resource Allocation

### Development Time (Hours/Week)
- Backend: 15-20 hours
- Extension: 10-15 hours
- Testing: 5-10 hours
- Documentation: 3-5 hours
- Community: 2-5 hours

### Budget Estimates
- Infrastructure: $50-100/month
  - Database hosting: $20
  - Backend hosting: $20
  - Redis: $10
  - Domain & SSL: $10
- AI API costs: $50-200/month
  - OpenAI: $30-100
  - Anthropic: $20-100
- Tools & Services: $30/month
  - Sentry monitoring
  - Email service
  - Analytics

**Total: ~$130-330/month**

---

## Risk Mitigation

### Technical Risks
- **Model loading slow**: Use smaller models, implement caching
- **API rate limits**: Implement queue system, batch requests
- **Extension compatibility**: Test across Chrome versions, fallback gracefully

### Business Risks
- **Low adoption**: Focus on ELTE first, get testimonials, iterate quickly
- **Competition**: Emphasize education over punishment, add unique features
- **Sustainability**: Start monetization early, seek university partnerships

---

## Next Immediate Actions

### This Week (Week 1)
1. ✅ Set up database with Alembic
2. ✅ Implement user authentication
3. ✅ Write unit tests for services
4. 🔄 Deploy backend to test server
5. 🔄 Start extension scaffolding

### This Month (Weeks 1-4)
1. Complete backend MVP
2. Build functional extension
3. Get 5 alpha testers from Data Science Club
4. Collect feedback and iterate

---

## Questions to Answer

- [ ] Which citation style to prioritize first? (APA most common)
- [ ] Local vs. cloud AI models for paraphrasing? (Start cloud, add local later)
- [ ] Freemium limit? (10 documents/month free, then $4.99)
- [ ] Which platforms after Google Docs? (Word Online, then Notion)
- [ ] Privacy approach? (End-to-end encryption option)

---

**Last Updated**: February 6, 2026
**Status**: MVP Development in Progress
**Next Milestone**: Beta Launch (Week 6)