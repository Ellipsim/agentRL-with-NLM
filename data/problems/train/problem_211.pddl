

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b4)
(ontable b2)
(on b3 b6)
(ontable b4)
(ontable b5)
(on b6 b5)
(on b7 b1)
(on b8 b7)
(clear b2)
(clear b3)
(clear b8)
)
(:goal
(and
(on b2 b8)
(on b3 b7)
(on b5 b2)
(on b6 b1)
(on b7 b5)
(on b8 b6))
)
)


