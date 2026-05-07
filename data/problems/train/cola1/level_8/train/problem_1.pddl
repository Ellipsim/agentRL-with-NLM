

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b5)
(on b4 b3)
(on b5 b7)
(ontable b6)
(on b7 b8)
(ontable b8)
(on b9 b4)
(ontable b10)
(clear b1)
(clear b2)
(clear b6)
(clear b9)
(clear b10)
)
(:goal
(and
(on b1 b8)
(on b3 b6)
(on b4 b7)
(on b5 b9)
(on b7 b3)
(on b9 b1)
(on b10 b4))
)
)


