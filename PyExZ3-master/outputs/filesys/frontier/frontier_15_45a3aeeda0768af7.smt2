(set-logic ALL)
; Frontier Constraint ID: 45a3aeeda0768af7
; Generated at: 2026-04-17 03:12:47
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2833)) (False)
(assert (not (= x 2833)))

; Query: ((== x 2834)) (False)
(assert (not (not (= x 2834))))

(check-sat)
(get-model)
