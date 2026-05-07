

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b6)
(ontable b2)
(on b3 b2)
(on b4 b3)
(on b5 b7)
(ontable b6)
(ontable b7)
(on b8 b5)
(clear b1)
(clear b4)
(clear b8)
)
(:goal
(and
(on b5 b2)
(on b6 b8)
(on b7 b4))
)
)


