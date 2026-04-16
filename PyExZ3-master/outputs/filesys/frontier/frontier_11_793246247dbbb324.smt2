(set-logic ALL)
; Constraint ID: 793246247dbbb324
; Generated at: 2026-04-16 11:47:24
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60376)) (False)
(assert (not (= x 60376)))

; Query: ((== x 60377)) (False)
(assert (not (not (= x 60377))))

(check-sat)
(get-model)
