(set-logic ALL)
; Constraint ID: f55f173b11b32476
; Generated at: 2026-04-16 04:18:59
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59329)) (False)
(assert (not (= x 59329)))

; Query: ((== x 59330)) (False)
(assert (not (not (= x 59330))))

(check-sat)
(get-model)
