

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b2)
(on b4 b1)
(ontable b5)
(ontable b6)
(on b7 b8)
(on b8 b4)
(clear b3)
(clear b5)
(clear b6)
(clear b7)
)
(:goal
(and
(on b1 b2)
(on b3 b6)
(on b4 b5))
)
)


