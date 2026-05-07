

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b6)
(on b2 b8)
(on b3 b1)
(ontable b4)
(on b5 b2)
(on b6 b5)
(ontable b7)
(ontable b8)
(clear b3)
(clear b4)
(clear b7)
)
(:goal
(and
(on b1 b6)
(on b2 b4)
(on b5 b8)
(on b7 b2)
(on b8 b1))
)
)


