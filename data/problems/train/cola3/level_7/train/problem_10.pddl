

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b8)
(on b2 b1)
(ontable b3)
(ontable b4)
(ontable b5)
(on b6 b5)
(ontable b7)
(on b8 b7)
(clear b2)
(clear b3)
(clear b4)
(clear b6)
)
(:goal
(and
(on b1 b2)
(on b2 b6)
(on b4 b7)
(on b6 b4))
)
)


