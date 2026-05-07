

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b5)
(on b2 b8)
(ontable b3)
(ontable b4)
(on b5 b4)
(ontable b6)
(on b7 b2)
(ontable b8)
(clear b1)
(clear b3)
(clear b6)
(clear b7)
)
(:goal
(and
(on b1 b6)
(on b5 b3)
(on b6 b8)
(on b7 b1)
(on b8 b5))
)
)


