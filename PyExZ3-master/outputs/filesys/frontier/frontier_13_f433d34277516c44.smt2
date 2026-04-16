(set-logic ALL)
; Frontier Constraint ID: f433d34277516c44
; Generated at: 2026-04-16 15:26:57
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1330)) (False)
(assert (not (= x 1330)))

; Query: ((== x 1331)) (False)
(assert (not (not (= x 1331))))

(check-sat)
(get-model)
