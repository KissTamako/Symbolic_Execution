(set-logic ALL)
; Constraint ID: c177c1229594e301
; Generated at: 2026-04-16 04:08:23
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59257)) (False)
(assert (not (= x 59257)))

; Query: ((== x 59258)) (False)
(assert (not (not (= x 59258))))

(check-sat)
(get-model)
