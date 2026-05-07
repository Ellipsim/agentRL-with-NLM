

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b10)
(ontable b2)
(ontable b3)
(on b4 b12)
(on b5 b7)
(ontable b6)
(on b7 b2)
(on b8 b9)
(on b9 b3)
(on b10 b4)
(on b11 b1)
(ontable b12)
(clear b5)
(clear b6)
(clear b8)
(clear b11)
)
(:goal
(and
(on b1 b6)
(on b2 b3)
(on b3 b12)
(on b4 b2)
(on b6 b11)
(on b7 b8)
(on b9 b10)
(on b10 b5)
(on b11 b7))
)
)


