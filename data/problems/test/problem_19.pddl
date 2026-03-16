

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b2)
(ontable b2)
(ontable b3)
(ontable b4)
(ontable b5)
(on b6 b1)
(ontable b7)
(on b8 b3)
(clear b4)
(clear b5)
(clear b6)
(clear b7)
(clear b8)
)
(:goal
(and
(on b1 b2)
(on b2 b3)
(on b3 b6)
(on b5 b8)
(on b6 b5)
(on b8 b7))
)
)


