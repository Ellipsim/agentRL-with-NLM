

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b5)
(on b2 b1)
(ontable b3)
(ontable b4)
(on b5 b3)
(on b6 b8)
(ontable b7)
(ontable b8)
(clear b2)
(clear b4)
(clear b6)
(clear b7)
)
(:goal
(and
(on b1 b8)
(on b3 b7)
(on b5 b3)
(on b6 b5)
(on b8 b2))
)
)


