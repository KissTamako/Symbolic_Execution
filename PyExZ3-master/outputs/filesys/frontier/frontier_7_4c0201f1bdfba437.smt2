(set-logic ALL)
; Constraint ID: 4c0201f1bdfba437
; Generated at: 2026-04-16 11:29:08
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59995)) (False)
(assert (not (= x 59995)))

; Query: ((== x 59996)) (False)
(assert (not (not (= x 59996))))

(check-sat)
(get-model)
