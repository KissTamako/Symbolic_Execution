(set-logic ALL)
; Path ID: 1fb4dc2608dc3c62
; Generated at: 2026-04-16 12:01:20
; Solver: Z3Wrapper
; Number of assertions: 12
; Has query: True

(declare-const k Int)
(declare-const se Int)

; ((== k 4944)) (False)
(assert (not (= k 4944)))
; ((== k 430)) (False)
(assert (not (= k 430)))
; ((== k 95)) (False)
(assert (not (= k 95)))
; ((== k 6)) (False)
(assert (not (= k 6)))
; ((== k 4)) (False)
(assert (not (= k 4)))
; ((== k 0)) (False)
(assert (not (= k 0)))
; ((> k 6)) (False)
(assert (not (> k 6)))
; ((== k 6)) (False)
(assert (not (= k 6)))
; ((> k 4)) (True)
(assert (> k 4))
; ((== k 4)) (False)
(assert (not (= k 4)))
; ((> k 95)) (False)
(assert (not (> k 95)))
; ((== k 95)) (False)
(assert (not (= k 95)))

; Query: ((== k 119101)) (False)
(assert (not (not (= k 119101))))

(check-sat)
(get-model)
