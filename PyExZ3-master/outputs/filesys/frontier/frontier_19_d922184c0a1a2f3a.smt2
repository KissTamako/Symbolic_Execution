(set-logic ALL)
; Constraint ID: d922184c0a1a2f3a
; Generated at: 2026-04-16 11:49:33
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60463)) (False)
(assert (not (= x 60463)))

; Query: ((== x 60464)) (False)
(assert (not (not (= x 60464))))

(check-sat)
(get-model)
