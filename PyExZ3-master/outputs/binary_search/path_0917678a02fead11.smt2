(set-logic ALL)
; Executed Path ID: 0917678a02fead11
; Generated at: 2026-04-16 16:02:49
; Solver: Z3Wrapper
; Number of predicates: 13
; Has query: False

(declare-const k Int)

; ((== k 95)) (False)
(assert (not (= k 95)))
; ((> k 95)) (False)
(assert (not (> k 95)))
; ((== k 4)) (False)
(assert (not (= k 4)))
; ((> k 4)) (True)
(assert (> k 4))
; ((== k 6)) (False)
(assert (not (= k 6)))
; ((> k 6)) (False)
(assert (not (> k 6)))
; ((== k 0)) (False)
(assert (not (= k 0)))
; ((== k 4)) (False)
(assert (not (= k 4)))
; ((== k 6)) (False)
(assert (not (= k 6)))
; ((== k 95)) (False)
(assert (not (= k 95)))
; ((== k 430)) (False)
(assert (not (= k 430)))
; ((== k 4944)) (False)
(assert (not (= k 4944)))
; ((== k 119101)) (False)
(assert (not (= k 119101)))

(check-sat)
(get-model)
